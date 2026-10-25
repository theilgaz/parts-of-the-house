// Kolay Ev: dil seçimi + katlanır 3D model (three.js r128, global THREE)
(function () {
  // ---------- dil ----------
  // Türkçe metinler HTML'de; İngilizce burada. Türkçeye dönüş için ilk metinler saklanır.
  const EN = {
    "nav.download": "Download", "nav.steps": "Steps", "nav.video": "Video script",
    "hero.eyebrow": "Free · Open source · Parts of the House",
    "hero.title": "A fold-up paper house for the Parts of the House lesson",
    "hero.lead": "One A3 sheet. Print it in colour, cut, fold and glue. Kitchen, living room, bathroom, bedroom and garden are all there, labelled in English and ready for a video.",
    "cta.a3": "Download A3 template (PDF)", "cta.a4": "A4 template", "cta.guide": "Instruction sheet",
    "facts.time": "Time", "facts.timev": "~40 min", "facts.size": "Size", "facts.paper": "Paper", "facts.paperv": "A3 matte coated card 250-300 gsm",
    "viewer.hint": "Drag to turn · Scroll to zoom", "viewer.play": "Fold it", "viewer.flat": "Flat sheet",
    "sheet.title": "What is on the sheet", "sheet.lead": "Everything fits on one page and is already in colour. Colouring is optional.",
    "rooms.kitchen": "cupboards, cooker, fridge, table", "rooms.living": "TV, sofa, rug, lamp", "rooms.bath": "shower, sink, mirror, bathtub",
    "rooms.bed": "bed, window, bookshelf", "rooms.garden": "grass, path, tree, flowers",
    "sheet.note": "8 pieces: the house (one piece), the upstairs floor and 6 standing items.",
    "steps.title": "How to build it", "steps.lead": "An adult does the cutting; the child folds and places the pieces.",
    "s1.h": "Print", "s1.p": "A3, colour, matte coated card 250-300 gsm. Scale 100% (actual size). No A3? Print the A4 file.",
    "s2.h": "Cut", "s2.p": "Cut along the solid lines. The house is one piece; next to it are the upstairs floor and 6 items.",
    "s3.h": "Score and fold", "s3.p": "Run an empty ballpoint pen along the dashed lines with a ruler. Fold with the printed side inside.",
    "s4.h": "Stand it up", "s4.p": "Tuck the grey tabs under the side walls inwards and glue them under the floor.",
    "s5.h": "Upstairs", "s5.p": "Fold the 3 tabs of the upstairs floor up and glue them onto the white strips on the walls.",
    "s6.h": "Furniture", "s6.p": "Fold the bottom tabs back and glue them to the floor. Bed and bathtub upstairs, table and sofa downstairs, tree and flowers in the garden.",
    "video.title": "Video script", "video.lead": "About 45 seconds when read slowly. Point at each room while saying its sentence.",
    "video.say": "Sentence", "video.pron": "Pronunciation", "video.dh": "",
    "tips.1": "Film in daylight, facing a window.", "tips.2": "Keep the phone landscape and steady; a stack of books works.",
    "tips.3": "Turn the TV off and keep the phone within 1 metre of the child.", "tips.4": "Write the sentences large and tape them behind the camera; no need to memorise.",
    "foot.license": "Open source. Code under MIT, template and images under CC BY 4.0: copy, print, share and remix, just credit the source.",
    "foot.repo": "Source code and contributions: GitHub",
  };
  const FILES = {
    tr: { a3: "downloads/kolay-ev-A3-tr.pdf", a4: "downloads/kolay-ev-A4-tr.pdf", guide: "downloads/talimat-tr.pdf", img: "assets/preview-tr.png" },
    en: { a3: "downloads/kolay-ev-A3-en.pdf", a4: "downloads/kolay-ev-A4-en.pdf", guide: "downloads/instructions-en.pdf", img: "assets/preview-en.png" },
  };
  const STAGES = {
    tr: ["Düz kağıt", "Arka duvar kalkıyor", "Yan duvarlar katlanıyor", "Üst kat ve eşyalar", "Bitmiş ev"],
    en: ["Flat sheet", "Back wall goes up", "Side walls fold in", "Upstairs and furniture", "Finished house"],
  };
  const TR = {};
  document.querySelectorAll("[data-i18n]").forEach((el) => { TR[el.dataset.i18n] = el.textContent; });
  let lang = "tr";

  function setLang(l) {
    lang = l;
    document.documentElement.lang = l;
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const k = el.dataset.i18n;
      el.textContent = l === "en" ? (EN[k] ?? TR[k]) : TR[k];
    });
    document.querySelectorAll("[data-dl]").forEach((a) => { a.href = FILES[l][a.dataset.dl]; });
    const img = document.getElementById("sheetimg");
    img.src = FILES[l].img; document.getElementById("sheetlink").href = FILES[l].img;
    img.alt = l === "en" ? "The whole A3 template" : "A3 şablonun tamamı";
    document.querySelectorAll(".lang button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === l)));
    try { localStorage.setItem("kolay-ev-lang", l); } catch (e) { /* depolama kapalı olabilir */ }
    if (window.__foldApply) window.__foldApply();
  }
  document.querySelectorAll(".lang button").forEach((b) => b.addEventListener("click", () => setLang(b.dataset.lang)));
  let saved = null;
  try { saved = localStorage.getItem("kolay-ev-lang"); } catch (e) { /* yok say */ }
  setLang(saved || ((navigator.language || "tr").toLowerCase().startsWith("tr") ? "tr" : "en"));

  // ---------- 3D ----------
  if (!window.THREE || !THREE.OrbitControls) return;
  const stage = document.getElementById("stage");
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  stage.prepend(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1, 1, 5000);
  camera.position.set(230, 250, 440);
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.target.set(0, 80, 40);
  controls.enableDamping = true;
  controls.enablePan = false;
  controls.minDistance = 180;
  controls.maxDistance = 1100;
  controls.maxPolarAngle = 1.48;

  scene.add(new THREE.HemisphereLight(0xffffff, 0xcdbfa8, 0.8));
  const sun = new THREE.DirectionalLight(0xffffff, 0.65);
  sun.position.set(160, 320, 260);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -300, right: 300, top: 300, bottom: -300, near: 10, far: 1200 });
  sun.shadow.bias = -0.0005;
  scene.add(sun);

  const table = new THREE.Mesh(new THREE.PlaneGeometry(3000, 3000), new THREE.MeshStandardMaterial({ color: 0xe9dcc8, roughness: 1 }));
  table.rotation.x = -Math.PI / 2;
  table.receiveShadow = true;
  scene.add(table);
  function applyTheme() {
    const tc = getComputedStyle(document.documentElement).getPropertyValue("--table").trim() || "#e9dcc8";
    table.material.color.set(tc);
    scene.background = new THREE.Color(tc).lerp(new THREE.Color(0xffffff), 0.3);
    scene.fog = new THREE.Fog(scene.background.getHex(), 650, 1500);
  }
  applyTheme();
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", applyTheme);
  new MutationObserver(applyTheme).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

  const loader = new THREE.TextureLoader();
  const tex = (k) => {
    const t = loader.load(`assets/tex/${k}.png`);
    t.encoding = THREE.sRGBEncoding;
    t.anisotropy = renderer.capabilities.getMaxAnisotropy();
    return t;
  };
  const front = (k, extra) => new THREE.MeshStandardMaterial(Object.assign({ map: tex(k), roughness: 0.8, alphaTest: 0.5, side: THREE.FrontSide }, extra || {}));
  const paperBack = new THREE.MeshStandardMaterial({ color: 0xf4f1ea, roughness: 0.9, side: THREE.BackSide });
  function sheet(geom, k) {
    const g = new THREE.Group();
    const a = new THREE.Mesh(geom, front(k));
    const b = new THREE.Mesh(geom, paperBack);
    a.castShadow = b.castShadow = true;
    a.receiveShadow = true;
    g.add(a, b);
    return g;
  }

  // Ölçüler mm: duvar 170 x 144, çatı tepesi 197, derinlik 50, bahçe 40, kat 72
  const floorG = new THREE.PlaneGeometry(170, 90);
  floorG.rotateX(-Math.PI / 2);
  floorG.translate(0, 0.3, 45);
  const floor = new THREE.Mesh(floorG, front("floor"));
  floor.receiveShadow = true;
  scene.add(floor);

  const shp = new THREE.Shape();
  shp.moveTo(-85, 0); shp.lineTo(85, 0); shp.lineTo(85, 144); shp.lineTo(0, 197); shp.lineTo(-85, 144); shp.closePath();
  const backG = new THREE.ShapeGeometry(shp);
  const pos = backG.attributes.position, uv = backG.attributes.uv;
  for (let i = 0; i < pos.count; i++) uv.setXY(i, (pos.getX(i) + 85) / 170, pos.getY(i) / 197);
  uv.needsUpdate = true;
  const backPivot = new THREE.Group();
  backPivot.position.set(0, 0.3, 0);
  scene.add(backPivot);
  backPivot.add(sheet(backG, "back"));

  const leftPivot = new THREE.Group();
  leftPivot.position.set(-85, 0, 0);
  backPivot.add(leftPivot);
  const lg = new THREE.PlaneGeometry(50, 144);
  lg.translate(-25, 72, 0);
  leftPivot.add(sheet(lg, "left"));
  const rightPivot = new THREE.Group();
  rightPivot.position.set(85, 0, 0);
  backPivot.add(rightPivot);
  const rg = new THREE.PlaneGeometry(50, 144);
  rg.translate(25, 72, 0);
  rightPivot.add(sheet(rg, "right"));

  const parts = [];
  const midG = new THREE.PlaneGeometry(168, 49);
  midG.rotateX(-Math.PI / 2);
  const midM = front("mid", { transparent: true, side: THREE.DoubleSide });
  const mid = new THREE.Mesh(midG, midM);
  mid.castShadow = mid.receiveShadow = true;
  scene.add(mid);
  parts.push({ obj: mid, mat: midM, to: new THREE.Vector3(0, 72, 24.5), delay: 0 });
  [["bed", 50, 26, -42, 72, 28], ["tub", 46, 24, 40, 72, 24], ["table", 40, 24, -40, 0, 32],
   ["sofa", 52, 25, 42, 0, 36], ["tree", 34, 60, -52, 0, 72], ["bush", 24, 18, 52, 0, 76]].forEach(([k, w, h, x, y, z], i) => {
    const g = new THREE.PlaneGeometry(w, h);
    g.translate(0, h / 2, 0);
    const m = front(k, { transparent: true, side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(g, m);
    scene.add(mesh);
    parts.push({ obj: mesh, mat: m, to: new THREE.Vector3(x, y + 0.4, z), delay: 0.12 + i * 0.1 });
  });

  const clamp = (v) => Math.max(0, Math.min(1, v));
  const ease = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
  const nameEl = document.getElementById("stagename");
  const slider = document.getElementById("fold");
  let p = 1, target = 1;
  function apply() {
    const f1 = ease(clamp(p / 0.4)), f2 = ease(clamp((p - 0.4) / 0.3)), f3 = clamp((p - 0.7) / 0.3);
    backPivot.rotation.x = -(1 - f1) * Math.PI / 2;
    leftPivot.rotation.y = f2 * Math.PI / 2;
    rightPivot.rotation.y = -f2 * Math.PI / 2;
    parts.forEach((pt) => {
      const e = ease(clamp((f3 - pt.delay) / (1 - pt.delay)));
      pt.obj.visible = e > 0.001;
      pt.obj.position.set(pt.to.x, pt.to.y + (1 - e) * 90, pt.to.z);
      pt.mat.opacity = e;
    });
    const s = STAGES[lang];
    nameEl.textContent = p < 0.001 ? s[0] : p < 0.4 ? s[1] : p < 0.7 ? s[2] : p < 0.999 ? s[3] : s[4];
  }
  window.__foldApply = apply;
  slider.addEventListener("input", () => { target = p = slider.value / 1000; apply(); });
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.getElementById("play").addEventListener("click", () => { p = reduce ? 1 : 0; target = 1; apply(); });
  document.getElementById("flat").addEventListener("click", () => { target = 0; if (reduce) p = 0; apply(); });

  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(stage);
  resize();
  apply();

  let last = performance.now();
  renderer.setAnimationLoop((now) => {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    if (p !== target) {
      const d = target - p, step = (dt / 4.5) * (target < p ? 2 : 1);
      p = Math.abs(d) <= step ? target : p + Math.sign(d) * step;
      slider.value = Math.round(p * 1000);
      apply();
    }
    controls.update();
    renderer.render(scene, camera);
  });
})();
