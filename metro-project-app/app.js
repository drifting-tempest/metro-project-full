const DATA = window.METRO_DATA;
/* =========================================================================
   DATA
   ========================================================================= */
// DATA is loaded from data.json and injected before this script runs (see index.html)
const LINES = DATA.lines;                 // { lineName: {stations:[...], color} }
const EDGE_LISTS = DATA.edges;             // { lineName: [{a,b,distance}] }
const STATIONS = DATA.stations;            // { name: {lat,lng,ja,code} }
const SPECIAL_TRANSFER = new Set(DATA.specialTransferStations); // Kuramae, Higashi-nihombashi, Bakuro-yokoyama
const TRAM_LINE = "Tokyo Sakura Tram";

// we are estimating speed based on travel time.
// metro/liner ~32 km/h incl. dwell, tram ~13 km/h incl. stops. (THIS ESTIMATION PART IS LOWK CLAUDE)
const SPEED_KMH = { metro: 32, tram: 13 };
const DWELL_MIN_METRO = 0.6;   // per intermediate stop
const TRANSFER_PENALTY_MIN = 4; // walking + wait time added per line change

/* Build a station -> [{line, neighbor, distance}] adjacency graph merging all lines */
const graph = {}; // name -> [{to, dist, line}]
function addEdge(a,b,dist,line){
  (graph[a] ||= []).push({to:b, dist, line});
  (graph[b] ||= []).push({to:a, dist, line});
}
for (const [lineName, edges] of Object.entries(EDGE_LISTS)){
  for (const e of edges) addEdge(e.a, e.b, e.distance, lineName);
}
// lines transfer point --> the two lines meet here)
const HUB = DATA.transferHub; // {a:'Nishi-sugamo', b:'Shin-koshinzuka'}
addEdge(HUB.a, HUB.b, 0.0, "__TRANSFER__");

const ALL_STATION_NAMES = Object.keys(STATIONS).sort();

// THE PRICE STUFF USING price.py 
const FARE_TABLES = {
  adult_ic:      {4:178, 9:220, 15:272, 21:325, 27:377, 46:430},
  adult_ticket:  {4:180, 9:220, 15:280, 21:330, 27:380, 46:430},
  children_ic:      {4:89, 9:110, 15:136, 21:162, 27:188, 46:215},
  children_ticket:  {4:90, 9:110, 15:140, 21:170, 27:190, 46:220},
};
const SAKURA_FLAT = { adult_ic:168, adult_ticket:170, children_ic:84, children_ticket:90 };
const FARE_ORDER = ["adult_ic","adult_ticket","children_ic","children_ticket"];

function fareByKm(km){
  // replicating price.fare() to get all returns in type of yen 
  const out = {};
  for (const type of FARE_ORDER){
    const table = FARE_TABLES[type];
    let val = null;
    for (const distKey of [4,9,15,21,27,46]){
      if (km <= distKey){ val = table[distKey]; break; }
    }
    if (val === null) val = table[46];
    out[type] = val;
  }
  return out;
}
function fareSakura(kmSakura, kmToei){
  // replicating price.fare_sakura()  
  const toei = fareByKm(kmToei);
  const out = {};
  for (const type of FARE_ORDER) out[type] = SAKURA_FLAT[type] + toei[type];
  return out;
}
function fareTransfer(kmBefore, kmAfter){
  // mirrors price.fare_transfer(): two separate fares stacked (Kuramae / Higashi-Nihombashi / Bakuro-yokoyama rule)
  const f1 = fareByKm(kmBefore), f2 = fareByKm(kmAfter);
  const out = {};
  for (const type of FARE_ORDER) out[type] = f1[type] + f2[type];
  return out;
}

//  finding the path using the dijkstra for loopless shortest paths

function dijkstra(start, end, blockedEdges){
  blockedEdges = blockedEdges || new Set(); // set of "A|B" strings to exclude
  const dist = {}, prevNode = {}, prevLine = {};
  const visited = new Set();
  dist[start] = 0;
  const pq = [[0, start]];
  while (pq.length){
    pq.sort((a,b)=>a[0]-b[0]);
    const [d, u] = pq.shift();
    if (visited.has(u)) continue;
    visited.add(u);
    if (u === end) break;
    for (const edge of (graph[u]||[])){
      const key1 = u+"|"+edge.to, key2 = edge.to+"|"+u;
      if (blockedEdges.has(key1) || blockedEdges.has(key2)) continue;
      const nd = d + edge.dist;
      if (dist[edge.to] === undefined || nd < dist[edge.to]){
        dist[edge.to] = nd;
        prevNode[edge.to] = u;
        prevLine[edge.to] = edge.line;
        pq.push([nd, edge.to]);
      }
    }
  }
  if (dist[end] === undefined) return null;
  const stations = [end];
  const lines = [];
  let cur = end;
  while (cur !== start){
    lines.unshift(prevLine[cur]);
    cur = prevNode[cur];
    stations.unshift(cur);
  }
  return { stations, lines, distance: dist[end] };
}

function pathKey(p){ return p.stations.join(">"); }

function kShortestPaths(start, end, K){
  const A = [];
  const first = dijkstra(start, end);
  if (!first) return [];
  A.push(first);
  const B = []; // candidates: {path, key}

  for (let k=1; k<K; k++){
    const prevPath = A[k-1];
    for (let i=0; i<prevPath.stations.length-1; i++){
      const spurNode = prevPath.stations[i];
      const rootStations = prevPath.stations.slice(0, i+1);

      const blocked = new Set();
      for (const p of A){
        if (p.stations.length > i && rootStations.every((s,idx)=>p.stations[idx]===s)){
          blocked.add(p.stations[i] + "|" + p.stations[i+1]);
        }
      }
      // also remove root nodes (except spur node) from being revisited: simulate by blocking all their edges
      // basically we avoiding the loop
      const removedNodeEdges = new Set();
      for (let j=0;j<rootStations.length-1;j++){
        const n = rootStations[j];
        for (const e of (graph[n]||[])) removedNodeEdges.add(n+"|"+e.to);
      }
      const totalBlocked = new Set([...blocked, ...removedNodeEdges]);

      const spurResult = dijkstraFrom(spurNode, end, totalBlocked, new Set(rootStations.slice(0,-1)));
      if (!spurResult) continue;

      const totalStations = rootStations.slice(0,-1).concat(spurResult.stations);
      const rootDist = pathDistanceOf(rootStations);
      const totalDist = rootDist + spurResult.distance;
      const totalLines = linesForStations(totalStations);

      const cand = { stations: totalStations, lines: totalLines, distance: totalDist };
      const key = pathKey(cand);
      if (!A.some(p=>pathKey(p)===key) && !B.some(b=>pathKey(b)===key)){
        B.push(cand);
      }
    }
    if (B.length === 0) break;
    B.sort((a,b)=>a.distance-b.distance);
    A.push(B.shift());
  }
  return A;
}
// additional logic from dijkstra stuff that also forbids revisiting nodes already used in the root path
function dijkstraFrom(start, end, blockedEdges, forbiddenNodes){
  const dist = {}, prevNode = {}, prevLine = {};
  const visited = new Set();
  dist[start] = 0;
  const pq = [[0, start]];
  while (pq.length){
    pq.sort((a,b)=>a[0]-b[0]);
    const [d,u] = pq.shift();
    if (visited.has(u)) continue;
    visited.add(u);
    if (u === end) break;
    for (const edge of (graph[u]||[])){
      if (forbiddenNodes.has(edge.to) && edge.to !== end) continue;
      const key1 = u+"|"+edge.to;
      if (blockedEdges.has(key1)) continue;
      const nd = d + edge.dist;
      if (dist[edge.to]===undefined || nd < dist[edge.to]){
        dist[edge.to]=nd; prevNode[edge.to]=u; prevLine[edge.to]=edge.line;
        pq.push([nd, edge.to]);
      }
    }
  }
  if (dist[end]===undefined) return null;
  const stations=[end], lines=[];
  let cur=end;
  while(cur!==start){ lines.unshift(prevLine[cur]); cur=prevNode[cur]; stations.unshift(cur); }
  return {stations, lines, distance: dist[end]};
}
function pathDistanceOf(stations){
  let total=0;
  for (let i=0;i<stations.length-1;i++){
    const edges = graph[stations[i]]||[];
    const e = edges.find(e=>e.to===stations[i+1]);
    total += e ? e.dist : 0;
  }
  return total;
}
function linesForStations(stations){
  const lines=[];
  for (let i=0;i<stations.length-1;i++){
    const edges = graph[stations[i]]||[];
    const e = edges.find(e=>e.to===stations[i+1]);
    lines.push(e ? e.line : "?");
  }
  return lines;
}

// the section for route, fare, time and transfer (the summary part)
function summarizeRoute(route){
  const { stations, lines, distance } = route;

  // collapse consecutive identical lines into "legs" so that we can make it like steps
  const legs = [];
  for (let i=0;i<lines.length;i++){
    const line = lines[i];
    if (legs.length && legs[legs.length-1].line === line){
      legs[legs.length-1].to = stations[i+1];
      legs[legs.length-1].km += pathDistanceOf([stations[i], stations[i+1]]);
      legs[legs.length-1].stops++;
    } else {
      legs.push({ line, from: stations[i], to: stations[i+1], km: pathDistanceOf([stations[i],stations[i+1]]), stops:1 });
    }
  }

  const transferStations = [];
  for (let i=1;i<legs.length;i++) transferStations.push(legs[i].from);

  const usesTram = legs.some(l=>l.line===TRAM_LINE);
  const kmTram = legs.filter(l=>l.line===TRAM_LINE).reduce((s,l)=>s+l.km,0);
  const kmToei = legs.filter(l=>l.line!==TRAM_LINE && l.line!=="__TRANSFER__").reduce((s,l)=>s+l.km,0);

  // finding the transfer station
  let specialSplit = null;
  for (const st of transferStations){
    if (SPECIAL_TRANSFER.has(st)){ specialSplit = st; break; }
  }

  let fares, fareMode;
  if (specialSplit){
    const idx = stations.indexOf(specialSplit);
    const kmBefore = pathDistanceOf(stations.slice(0, idx+1));
    const kmAfter = pathDistanceOf(stations.slice(idx));
    fares = fareTransfer(kmBefore, kmAfter);
    fareMode = `Split fare via ${specialSplit}`;
  } else if (usesTram){
    fares = fareSakura(kmTram, kmToei);
    fareMode = "Sakura Tram combination fare";
  } else {
    fares = fareByKm(distance);
    fareMode = "Standard shortest-route fare";
  }

  // estimating time
  let minutes = 0;
  for (const leg of legs){
    const speed = leg.line===TRAM_LINE ? SPEED_KMH.tram : SPEED_KMH.metro;
    minutes += (leg.km / speed) * 60;
    minutes += Math.max(0, leg.stops-1) * DWELL_MIN_METRO;
  }
  minutes += Math.max(0, legs.length-1) * TRANSFER_PENALTY_MIN;

  return { stations, lines, legs, distance, transferStations, fares, fareMode, minutes, usesTram };
}

/* =========================================================================
   UI WIRING
   ========================================================================= */
const stationListEl = document.getElementById('stationList');
ALL_STATION_NAMES.forEach(n=>{
  const opt = document.createElement('option'); opt.value = n; stationListEl.appendChild(opt);
});

let fareType = "adult_ic";
document.getElementById('fareToggle').addEventListener('click', e=>{
  const btn = e.target.closest('button'); if(!btn) return;
  [...btn.parentElement.children].forEach(b=>b.classList.remove('active'));
  btn.classList.add('active'); fareType = btn.dataset.v;
  if (window.__lastRoutes) renderResults(window.__lastRoutes);
});

document.getElementById('swapBtn').addEventListener('click', ()=>{
  const f = document.getElementById('fromInput'), t = document.getElementById('toInput');
  [f.value, t.value] = [t.value, f.value];
});

document.getElementById('findBtn').addEventListener('click', runSearch);

function runSearch(){
  const from = document.getElementById('fromInput').value.trim();
  const to = document.getElementById('toInput').value.trim();
  const resultsEl = document.getElementById('results');

  if (!STATIONS[from] || !STATIONS[to]){
    resultsEl.innerHTML = `<div class="empty-state">Station not recognized. Check spelling — pick from the suggestion list.</div>`;
    return;
  }
  if (from === to){
    resultsEl.innerHTML = `<div class="empty-state">Pick two different stations.</div>`;
    return;
  }

  const raw = kShortestPaths(from, to, 3);
  if (!raw.length){
    resultsEl.innerHTML = `<div class="empty-state">No route found.</div>`;
    return;
  }
  const routes = raw.map(summarizeRoute);
  window.__lastRoutes = routes;
  renderResults(routes);
  drawRouteOnMap(routes[0]);
  selectCard(0);
}

function lineChip(line){
  const color = line===TRAM_LINE ? "var(--sakura)" : (LINES[line] ? LINES[line].color : "#666");
  return `<span class="chip" style="background:${color}">${line.replace(' Line','').replace('Tokyo ','')}</span>`;
}

function renderResults(routes){
  const el = document.getElementById('results');
  el.innerHTML = "";
  routes.forEach((r, idx)=>{
    const card = document.createElement('div');
    card.className = 'route-card' + (idx===0 ? ' selected':'');
    card.dataset.idx = idx;
    const lineSet = [...new Set(r.legs.map(l=>l.line))];
    const yen = r.fares[fareType];
    card.innerHTML = `
      <div class="rank"><span>${idx===0?'<b>FASTEST</b>':'ALTERNATE '+(idx+1)}</span><span>${r.transferStations.length} transfer${r.transferStations.length!==1?'s':''}</span></div>
      <div class="headline">
        <span class="time">${Math.round(r.minutes)} min</span>
        <span class="dist">${r.distance.toFixed(2)} km · ${r.stations.length-1} stops</span>
      </div>
      <div class="lines">${lineSet.map(lineChip).join('')}</div>
      <div class="fare-row"><span class="lbl">${fareLabel(fareType)}</span><span>¥${yen}</span></div>
      ${r.fareMode.startsWith('Split')||r.fareMode.startsWith('Sakura') ? `<div class="transfer-note">${r.fareMode}</div>` : ""}
    `;
    card.addEventListener('click', ()=>{ selectCard(idx); drawRouteOnMap(r); showRouteDetail(r); });
    el.appendChild(card);
  });
  showRouteDetail(routes[0]);
}
function fareLabel(v){
  return {adult_ic:"Adult · IC", adult_ticket:"Adult · Ticket", children_ic:"Child · IC", children_ticket:"Child · Ticket"}[v];
}
function selectCard(idx){
  document.querySelectorAll('.route-card').forEach(c=>c.classList.toggle('selected', +c.dataset.idx===idx));
}

// station and route details 
function showRouteDetail(r){
  const el = document.getElementById('detailPanel');
  const stepsHtml = r.legs.map(leg=>{
    const color = leg.line===TRAM_LINE ? "var(--sakura)" : (LINES[leg.line]?LINES[leg.line].color:"#666");
    return `<li><span class="dot" style="background:${color}"></span>
      <span><b>${leg.from}</b> → <b>${leg.to}</b> <span style="color:var(--muted)">(${leg.stops} stop${leg.stops!==1?'s':''}, ${leg.km.toFixed(2)} km)</span></span>
      <span class="via">${leg.line.replace('Tokyo ','')}</span></li>`;
  }).join('');
  const fareRows = FARE_ORDER.map(t=>`<tr><td class="k">${fareLabel(t)}</td><td>¥${r.fares[t]}</td></tr>`).join('');
  el.innerHTML = `
    <h3>${r.stations[0]} → ${r.stations[r.stations.length-1]}</h3>
    <div class="ja">${r.distance.toFixed(2)} km · ~${Math.round(r.minutes)} min · ${r.fareMode}</div>
    <ul class="step-list">${stepsHtml}</ul>
    <table style="margin-top:12px;">${fareRows}</table>
  `;
}

function showStationDetail(name){
  const s = STATIONS[name];
  if (!s) return;
  const linesHere = Object.entries(LINES).filter(([_,v])=>v.stations.includes(name)).map(([k])=>k);
  const el = document.getElementById('detailPanel');
  el.innerHTML = `
    <h3>${name}</h3>
    <div class="ja">${s.ja || ''} ${s.code ? '· '+s.code : ''}</div>
    <table>
      <tr><td class="k">Lines</td><td>${linesHere.map(lineChip).join(' ')}</td></tr>
      <tr><td class="k">Coordinates</td><td>${s.lat.toFixed(5)}, ${s.lng.toFixed(5)}</td></tr>
    </table>
  `;
}

// everything about the maps
// claude magic and so much trial and error
const map = L.map('map', {zoomControl:true}).setView([35.69, 139.76], 12);
const tileNormal = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom:19, attribution:'© OpenStreetMap contributors'
}).addTo(map);
const tileSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  maxZoom:19, attribution:'Tiles © Esri'
});

document.getElementById('baseToggle').addEventListener('click', e=>{
  const btn = e.target.closest('button'); if(!btn) return;
  [...btn.parentElement.children].forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  if (btn.dataset.v==='satellite'){ map.removeLayer(tileNormal); tileSat.addTo(map); }
  else { map.removeLayer(tileSat); tileNormal.addTo(map); }
});

// draw all line polylines (background, dim)
const lineLayerGroup = L.layerGroup().addTo(map);
for (const [name, info] of Object.entries(LINES)){
  const latlngs = info.stations.filter(s=>STATIONS[s]).map(s=>[STATIONS[s].lat, STATIONS[s].lng]);
  L.polyline(latlngs, {color: info.color, weight:3, opacity:.45}).addTo(lineLayerGroup);
}
// station markers
const markerByName = {};
for (const [name, s] of Object.entries(STATIONS)){
  const m = L.circleMarker([s.lat, s.lng], {
    radius:4, color:'#0d1117', weight:1, fillColor:'#c9d3dd', fillOpacity:.9
  }).addTo(map);
  m.bindTooltip(name, {direction:'top', opacity:.85});
  m.on('click', ()=> showStationDetail(name));
  markerByName[name] = m;
}

let routeLayer = null;
function drawRouteOnMap(route){
  if (routeLayer) map.removeLayer(routeLayer);
  routeLayer = L.layerGroup().addTo(map);

  for (let i=0;i<route.stations.length-1;i++){
    const a = route.stations[i], b = route.stations[i+1];
    if (!STATIONS[a] || !STATIONS[b]) continue;
    const line = route.lines[i];
    const c = line===TRAM_LINE ? "#C1328E" : (LINES[line] ? LINES[line].color : "#ff9a3c");
    L.polyline([[STATIONS[a].lat,STATIONS[a].lng],[STATIONS[b].lat,STATIONS[b].lng]], {
      color:c, weight:6, opacity:.95
    }).addTo(routeLayer);
  }
  // start / end markers
  const startS = STATIONS[route.stations[0]], endS = STATIONS[route.stations[route.stations.length-1]];
  L.circleMarker([startS.lat,startS.lng], {radius:8, color:'#0d1117', weight:2, fillColor:'#4fd1a5', fillOpacity:1}).addTo(routeLayer);
  L.circleMarker([endS.lat,endS.lng], {radius:8, color:'#0d1117', weight:2, fillColor:'#ff9a3c', fillOpacity:1}).addTo(routeLayer);
  // transfer markers
  for (const st of route.transferStations){
    const s = STATIONS[st];
    if (s) L.circleMarker([s.lat,s.lng], {radius:7, color:'#fff', weight:2, fillColor:'#0d1117', fillOpacity:1}).addTo(routeLayer);
  }
  const bounds = L.latLngBounds(route.stations.filter(s=>STATIONS[s]).map(s=>[STATIONS[s].lat, STATIONS[s].lng]));
  map.fitBounds(bounds, {padding:[40,40]});
}

// legend
const legendEl = document.getElementById('legend');
legendEl.innerHTML = Object.entries(LINES).map(([name,info])=>
  `<div class="row"><span class="sw" style="background:${info.color}"></span>${name}</div>`
).join('') + `<div class="row"><span class="sw" style="background:#fff"></span>Transfer stop</div>`;

// clock
function tickClock(){
  document.getElementById('clock').textContent = new Date().toLocaleString('en-GB', {
    weekday:'short', hour:'2-digit', minute:'2-digit', second:'2-digit'
  }) + " · JST reference";
}
tickClock(); setInterval(tickClock, 1000);

// initial demo search
runSearch();
