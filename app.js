// ==========================================
// boAt Airdopes 3D Interactive Web Showcase
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. Video Playback Speed Controller
  const video = document.getElementById('mainCommercialVideo');
  const speedButtons = document.querySelectorAll('.speed-btn');

  if (video && speedButtons.length > 0) {
    speedButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        speedButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const speed = parseFloat(btn.getAttribute('data-speed'));
        video.playbackRate = speed;
      });
    });
  }

  // 2. Interactive Three.js 3D WebGL Earbuds Inspector
  initThreeJSViewer();
});

function initThreeJSViewer() {
  const container = document.getElementById('webglContainer');
  if (!container || typeof THREE === 'undefined') return;

  const width = container.clientWidth || 800;
  const height = container.clientHeight || 580;

  // Scene & Camera
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x06070a);
  scene.fog = new THREE.FogExp2(0x06070a, 0.08);

  const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
  camera.position.set(0, 0.5, 4.5);

  // WebGL Renderer
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
  scene.add(ambientLight);

  const keyLight = new THREE.DirectionalLight(0xffecd2, 3.5);
  keyLight.position.set(4, 5, 4);
  scene.add(keyLight);

  const rimLight = new THREE.DirectionalLight(0xff007f, 3.0);
  rimLight.position.set(-5, 4, -4);
  scene.add(rimLight);

  const cyanFill = new THREE.PointLight(0x00f2fe, 4.0, 15);
  cyanFill.position.set(-3, -1, 3);
  scene.add(cyanFill);

  // Materials
  const crimsonRedMat = new THREE.MeshPhysicalMaterial({
    color: 0xdd081e,
    metalness: 0.92,
    roughness: 0.15,
    clearcoat: 0.8,
    clearcoatRoughness: 0.1
  });

  const carbonMatteMat = new THREE.MeshStandardMaterial({
    color: 0x14161b,
    metalness: 0.25,
    roughness: 0.35
  });

  const gold24kMat = new THREE.MeshStandardMaterial({
    color: 0xf5b041,
    metalness: 1.0,
    roughness: 0.08
  });

  const rubyTipMat = new THREE.MeshPhysicalMaterial({
    color: 0x880512,
    transmission: 0.6,
    opacity: 0.85,
    transparent: true,
    roughness: 0.3,
    ior: 1.4
  });

  const cyanLedMat = new THREE.MeshBasicMaterial({
    color: 0x00f2fe
  });

  const pedestalMat = new THREE.MeshStandardMaterial({
    color: 0x0a0c10,
    metalness: 0.8,
    roughness: 0.12
  });

  // Group to hold Earbuds Duo & Stage
  const earbudGroup = new THREE.Group();
  scene.add(earbudGroup);

  // Helper to build 3D Earbud
  function createEarbud(mirror = 1) {
    const root = new THREE.Group();

    // 1. Rear Acoustic Shell
    const podGeo = new THREE.SphereGeometry(0.38, 32, 24);
    podGeo.scale(0.9, 1.1, 0.9);
    const pod = new THREE.Mesh(podGeo, crimsonRedMat);
    root.add(pod);

    // 2. Silicone Ear Tip
    const tipGeo = new THREE.ConeGeometry(0.32, 0.32, 32);
    tipGeo.rotateX(Math.PI / 2);
    tipGeo.rotateY(mirror * 0.4);
    const tip = new THREE.Mesh(tipGeo, rubyTipMat);
    tip.position.set(0.28 * mirror, 0.22, 0.22);
    root.add(tip);

    // 3. Gold Acoustic Bevel
    const bevelGeo = new THREE.TorusGeometry(0.18, 0.02, 16, 32);
    const bevel = new THREE.Mesh(bevelGeo, gold24kMat);
    bevel.position.set(0.24 * mirror, 0.18, 0.18);
    bevel.rotation.y = mirror * 0.4;
    root.add(bevel);

    // 4. Velvet Carbon Stem
    const stemGeo = new THREE.CylinderGeometry(0.11, 0.09, 1.25, 32);
    const stem = new THREE.Mesh(stemGeo, carbonMatteMat);
    stem.position.set(-0.12 * mirror, -0.65, 0);
    stem.rotation.z = mirror * 0.1;
    root.add(stem);

    // 5. 24K Gold Touch Zone & boAt Badge
    const badgeGeo = new THREE.BoxGeometry(0.08, 0.32, 0.04);
    const badge = new THREE.Mesh(badgeGeo, gold24kMat);
    badge.position.set(-0.13 * mirror, -0.45, 0.11);
    root.add(badge);

    // 6. Neon Cyan LED
    const ledGeo = new THREE.SphereGeometry(0.035, 16, 16);
    const led = new THREE.Mesh(ledGeo, cyanLedMat);
    led.position.set(-0.13 * mirror, -0.25, 0.11);
    root.add(led);

    // 7. Gold Pogo Contact Pins
    [-0.04, 0.04].forEach(off => {
      const pinGeo = new THREE.CylinderGeometry(0.025, 0.025, 0.08, 16);
      const pin = new THREE.Mesh(pinGeo, gold24kMat);
      pin.position.set(-0.12 * mirror + off, -1.26, 0);
      root.add(pin);
    });

    return root;
  }

  // Left & Right Earbuds in Hero Duo Formation
  const leftEarbud = createEarbud(-1);
  leftEarbud.position.set(-0.65, 0.3, 0);
  leftEarbud.rotation.set(0.15, -0.35, -0.15);
  earbudGroup.add(leftEarbud);

  const rightEarbud = createEarbud(1);
  rightEarbud.position.set(0.65, 0.3, 0);
  rightEarbud.rotation.set(0.15, 0.35, 0.15);
  earbudGroup.add(rightEarbud);

  // Pedestal Stage
  const pedGeo = new THREE.CylinderGeometry(3.5, 3.8, 0.25, 64);
  const ped = new THREE.Mesh(pedGeo, pedestalMat);
  ped.position.set(0, -1.4, 0);
  scene.add(ped);

  // Neon Rim on Pedestal
  const rimGeo = new THREE.TorusGeometry(3.5, 0.025, 16, 64);
  rimGeo.rotateX(Math.PI / 2);
  const rim = new THREE.Mesh(rimGeo, cyanLedMat);
  rim.position.set(0, -1.27, 0);
  scene.add(rim);

  // Mouse & Touch Orbit Controls
  let isDragging = false;
  let prevMousePos = { x: 0, y: 0 };
  let targetRotation = { x: 0, y: 0 };
  let currentRotation = { x: 0, y: 0 };
  let targetZoom = 4.5;

  const onPointerDown = (e) => {
    isDragging = true;
    prevMousePos = { x: e.clientX || e.touches[0].clientX, y: e.clientY || e.touches[0].clientY };
  };

  const onPointerMove = (e) => {
    if (!isDragging) return;
    const clientX = e.clientX || (e.touches && e.touches[0].clientX);
    const clientY = e.clientY || (e.touches && e.touches[0].clientY);
    if (clientX === undefined) return;

    const deltaX = clientX - prevMousePos.x;
    const deltaY = clientY - prevMousePos.y;

    targetRotation.y += deltaX * 0.008;
    targetRotation.x += deltaY * 0.008;
    targetRotation.x = Math.max(-0.6, Math.min(0.8, targetRotation.x));

    prevMousePos = { x: clientX, y: clientY };
  };

  const onPointerUp = () => {
    isDragging = false;
  };

  const onWheel = (e) => {
    e.preventDefault();
    targetZoom += e.deltaY * 0.003;
    targetZoom = Math.max(2.5, Math.min(7.0, targetZoom));
  };

  const dom = renderer.domElement;
  dom.addEventListener('mousedown', onPointerDown);
  dom.addEventListener('mousemove', onPointerMove);
  window.addEventListener('mouseup', onPointerUp);

  dom.addEventListener('touchstart', onPointerDown, { passive: false });
  dom.addEventListener('touchmove', onPointerMove, { passive: false });
  window.addEventListener('touchend', onPointerUp);
  dom.addEventListener('wheel', onWheel, { passive: false });

  // Handle Resize
  window.addEventListener('resize', () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  });

  // Animation Loop
  let clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate);
    const elapsedTime = clock.getElapsedTime();

    // Auto-rotation when idle
    if (!isDragging) {
      targetRotation.y += 0.003;
    }

    // Smooth Damping
    currentRotation.x += (targetRotation.x - currentRotation.x) * 0.08;
    currentRotation.y += (targetRotation.y - currentRotation.y) * 0.08;
    camera.position.z += (targetZoom - camera.position.z) * 0.08;

    earbudGroup.rotation.y = currentRotation.y;
    earbudGroup.rotation.x = currentRotation.x;

    // Harmonic Anti-Gravity Floating Bob
    leftEarbud.position.y = 0.3 + Math.sin(elapsedTime * 2.0) * 0.04;
    rightEarbud.position.y = 0.3 + Math.sin(elapsedTime * 2.0 + 0.5) * 0.04;

    renderer.render(scene, camera);
  }

  animate();
}
