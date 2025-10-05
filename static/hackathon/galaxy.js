import * as THREE from "https://cdn.skypack.dev/three@0.129.0";
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";

let scene, camera, renderer, controls;
let currentView = 'galaxy';
let currentSolarSystem = null;
let galaxyStars = [];
let solarSystems = [];
let planetInfoModal = null;
let navigationPanel = null;
let systemsListPanel = null;
let raycaster = new THREE.Raycaster();
let mouse = new THREE.Vector2();
let isAnimating = false;
let animationFrameId = null;

// Planet textures with fallback colors
const PLANET_TEXTURES = [
    { path: "./images/1.jpg", fallback: "#2E8B57" },
    { path: "./images/2.jpg", fallback: "#CD5C5C" },
    { path: "./images/3.jpg", fallback: "#FFD700" },
    { path: "./images/6.jpg", fallback: "#A9A9A9" },
    { path: "./images/7.jpg", fallback: "#DAA520" },
    { path: "./images/8.jpg", fallback: "#F4A460" },
    { path: "./images/9.jpg", fallback: "#87CEEB" },
    { path: "./images/10.jpg", fallback: "#1E90FF" },
    { path: "./images/11.jpg", fallback: "#DAA520" },
    { path: "./images/12.jpg", fallback: "#F4A460" },
    { path: "./images/13.jpg", fallback: "#87CEEB" },
    { path: "./images/14.jpg", fallback: "#1E90FF" },


];

// Galaxy configuration
const GALAXY_CONFIG = {
    radius: 4000,
    starCount: 1000,
    armCount: 32,
    armWidth: 0.8,
    coreRadius: 300,
    zSpread: 2000
};

// System types
const SYSTEM_TYPES = {
    SOLAR_LIKE: { minPlanets: 3, maxPlanets: 6, habitableZone: 0.3, moonChance: 0.6 },
    HOT_SYSTEM: { minPlanets: 1, maxPlanets: 3, habitableZone: 0.1, moonChance: 0.2 },
    COLD_SYSTEM: { minPlanets: 4, maxPlanets: 8, habitableZone: 0.5, moonChance: 0.7 },
    GAS_GIANT_SYSTEM: { minPlanets: 2, maxPlanets: 5, habitableZone: 0.4, moonChance: 0.8 }
};

// Camera animation states
const CAMERA_STATES = {
    GALAXY_VIEW: 'galaxy_view',
    SYSTEM_VIEW: 'system_view',
    PLANET_VIEW: 'planet_view',
    TRANSITION: 'transition'
};

let currentCameraState = CAMERA_STATES.GALAXY_VIEW;

function init() {
    console.log("Initializing 3D Galaxy...");
    
    // Hide loading screen
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
    
    // Create scene
    scene = new THREE.Scene();
    
    // Create camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 10000);
    camera.position.set(0, GALAXY_CONFIG.radius * 0.3, GALAXY_CONFIG.radius * 0.5);
    
    // Create renderer
    renderer = new THREE.WebGLRenderer({ 
        antialias: true, 
        alpha: true 
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    document.body.appendChild(renderer.domElement);
    
    // Add controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 20;
    controls.maxDistance = 5000;
    
    // Initialize interface
    initInterface();
    
    // Generate galaxy
    generateSpiralGalaxy();
    
    // Setup event handlers
    setupEventHandlers();
    
    // Update interface
    updateNavigationPanel();
    updateSystemsList();
    
    console.log("Initialization complete!");
    
    // Start animation
    animate();
}

function initInterface() {
    console.log("Initializing interface...");
    
    // Navigation panel
    navigationPanel = document.createElement('div');
    navigationPanel.id = 'navigation-panel';
    navigationPanel.innerHTML = `
        <div class="galaxy-view">
            <h3>Galaxy Map</h3>
            <p>Loading star systems...</p>
        </div>
    `;
    document.body.appendChild(navigationPanel);

    // Systems list panel
    systemsListPanel = document.createElement('div');
    systemsListPanel.id = 'systems-list-panel';
    systemsListPanel.innerHTML = `
        <div class="systems-list">
            <h3>Star Systems</h3>
            <div class="search-box">
                <input type="text" id="system-search" placeholder="Search systems...">
            </div>
            <div class="systems-container">
                <p>Loading systems...</p>
            </div>
        </div>
    `;
    document.body.appendChild(systemsListPanel);

    // Planet info modal
    planetInfoModal = document.createElement('div');
    planetInfoModal.id = 'planet-info-modal';
    planetInfoModal.innerHTML = `
        <div class="planet-modal">
            <div class="planet-header">
                <h2>Planet Information</h2>
            </div>
            <div class="planet-content">
                <p>Select a planet to view information</p>
            </div>
            <button class="close-btn">Close</button>
        </div>
    `;
    document.body.appendChild(planetInfoModal);

    // Controls hint
    const controlsHint = document.createElement('div');
    controlsHint.className = 'controls-hint';
    controlsHint.innerHTML = `
        <strong>Controls:</strong><br>
        • Click on stars to enter system<br>
        • 'I' key to zoom out<br>
        • Mouse wheel to zoom<br>
        • Click planets for close view
    `;
    document.body.appendChild(controlsHint);
    
    // Camera status
    const cameraStatus = document.createElement('div');
    cameraStatus.className = 'camera-status';
    cameraStatus.innerHTML = 'View: Galaxy';
    cameraStatus.id = 'camera-status';
    document.body.appendChild(cameraStatus);
    
    // Add event listener to close button
    const closeBtn = planetInfoModal.querySelector('.close-btn');
    closeBtn.addEventListener('click', () => {
        planetInfoModal.style.display = 'none';
    });
}

function generateSpiralGalaxy() {
    console.log("Generating spiral galaxy...");
    galaxyStars = [];
    solarSystems = [];
    
    for (let i = 0; i < GALAXY_CONFIG.starCount; i++) {
        // Spiral distribution
        const arm = Math.floor(Math.random() * GALAXY_CONFIG.armCount);
        const angle = (arm * 2 * Math.PI / GALAXY_CONFIG.armCount) + 
                     (Math.random() - 0.5) * GALAXY_CONFIG.armWidth;
        
        const distance = Math.pow(Math.random(), 1.5) * GALAXY_CONFIG.radius;
        
        // 3D distribution with chaotic deviations
        const x = Math.cos(angle) * distance + (Math.random() - 0.5) * 150;
        const z = Math.sin(angle) * distance + (Math.random() - 0.5) * 150;
        const y = (Math.random() - 0.5) * GALAXY_CONFIG.zSpread;
        
        const starSystem = createStarSystem(i, new THREE.Vector3(x, y, z));
        if (starSystem) {
            galaxyStars.push(starSystem.star);
            solarSystems.push(starSystem);
        }
    }
    
    console.log(`Generated ${solarSystems.length} star systems`);
}

function createStarSystem(index, position) {
    try {
        const systemType = getRandomSystemType();
        const starTemp = Math.floor(Math.random() * 15000) + 2500;
        const starRadius = 3 + Math.random() * 8;
        
        const starGeometry = new THREE.SphereGeometry(starRadius, 16, 16);
        const starColor = getStarColorFromTemperature(starTemp);
        const starMaterial = new THREE.MeshBasicMaterial({ 
            color: starColor
        });
        
        const star = new THREE.Mesh(starGeometry, starMaterial);
        star.position.copy(position);
        
        const systemName = generateSystemName(index);
        
        const system = {
            name: systemName,
            star: star,
            planets: [],
            position: position.clone(),
            type: systemType,
            data: {
                hostname: systemName,
                st_rad: (starRadius / 10).toFixed(3),
                st_teff: starTemp,
                sy_pnum: 0,
                ra: (position.x / 10).toFixed(3),
                dec: (position.z / 10).toFixed(3),
                sy_dist: (position.length() / 100).toFixed(2)
            }
        };
        
        // Generate planets
        const planetCount = systemType.minPlanets + Math.floor(Math.random() * (systemType.maxPlanets - systemType.minPlanets));
        system.data.sy_pnum = planetCount;
        
        for (let i = 0; i < planetCount; i++) {
            const planet = generatePlanetData(i, system);
            system.planets.push(planet);
        }
        
        star.userData = {
            type: 'star',
            system: system,
            name: systemName
        };
        
        scene.add(star);
        return system;
    } catch (error) {
        console.error("Error creating star system:", error);
        return null;
    }
}

function getRandomSystemType() {
    const types = Object.values(SYSTEM_TYPES);
    return types[Math.floor(Math.random() * types.length)];
}

function generateSystemName(index) {
    const prefixes = ['Kepler', 'HD', 'GJ', 'TOI', 'TRAPPIST', 'K2'];
    const numbers = ['-10', '-22', '-47', '-186', '-296'];
    return `${prefixes[Math.floor(Math.random() * prefixes.length)]}${numbers[Math.floor(Math.random() * numbers.length)]}`;
}

function getStarColorFromTemperature(temp) {
    if (temp > 10000) return new THREE.Color(0x9bb0ff);
    if (temp > 7500) return new THREE.Color(0xa6caff);
    if (temp > 6000) return new THREE.Color(0xfff4ea);
    if (temp > 5000) return new THREE.Color(0xfff2b8);
    if (temp > 3700) return new THREE.Color(0xffb86f);
    return new THREE.Color(0xff4b4b);
}

function generatePlanetData(index, system) {
    const orbitRadius = 15 + index * 12 + (Math.random() * 8 - 4);
    const planetSize = 0.5 + Math.random() * 4;
    const orbitalPeriod = 30 + index * 20 + Math.random() * 30;
    
    const orbitInclination = (Math.random() - 0.5) * 0.4;
    const axialTilt = Math.random() * Math.PI;
    const eccentricity = Math.random() * 0.15;
    
    const textureInfo = PLANET_TEXTURES[Math.floor(Math.random() * PLANET_TEXTURES.length)];
    const useTexture = false;

    const moonCount = Math.random() < system.type.moonChance ? Math.floor(Math.random() * 4) : 0;
    const moons = [];
    
    for (let m = 0; m < moonCount; m++) {
        moons.push(generateMoonData(m, planetSize));
    }
    
    return {
        pl_name: `${system.name} ${String.fromCharCode(98 + index)}`,
        pl_rade: (planetSize * 0.8).toFixed(3),
        pl_orbper: orbitalPeriod.toFixed(2),
        pl_orbeccen: eccentricity.toFixed(3),
        size: planetSize,
        orbitRadius: orbitRadius,
        revolutionSpeed: 0.3 + Math.random() * 1.5,
        rotationSpeed: 0.003 + Math.random() * 0.008,
        orbitInclination: orbitInclination,
        axialTilt: axialTilt,
        type: Math.random() > 0.6 ? 'gas' : 'rocky',
        temperature: Math.floor(Math.random() * 600) + 100,
        mass: (planetSize * 80 + Math.random() * 500).toFixed(0),
        texture: useTexture ? textureInfo.path : null,
        fallbackColor: textureInfo.fallback,
        moons: moons,
        description: generatePlanetDescription()
    };
}

function generateMoonData(index, planetSize) {
    const moonSize = planetSize * (0.1 + Math.random() * 0.15);
    return {
        name: `Moon ${index + 1}`,
        size: moonSize,
        orbitRadius: planetSize * 1.5 + Math.random() * planetSize * 2,
        revolutionSpeed: 3 + Math.random() * 4,
        rotationSpeed: 0.01 + Math.random() * 0.02
    };
}

function generatePlanetDescription() {
    const types = ['Earth-like world', 'Gas giant', 'Ice planet', 'Desert world', 'Ocean planet'];
    const features = ['with complex weather', 'with ring system', 'with multiple moons', 'tidally locked'];
    return `${types[Math.floor(Math.random() * types.length)]} ${features[Math.floor(Math.random() * features.length)]}`;
}

function createPlanetMesh(planetData) {
    const geometry = new THREE.SphereGeometry(planetData.size, 16, 16);
    const material = createFallbackMaterial(planetData);
    
    const planet = new THREE.Mesh(geometry, material);
    planet.userData = planetData;
    planet.rotation.z = planetData.axialTilt;
    
    return planet;
}

function createFallbackMaterial(planetData) {
    let color;
    
    if (planetData.fallbackColor) {
        color = new THREE.Color(planetData.fallbackColor);
    } else {
        // Color based on temperature and type
        if (planetData.temperature > 450) {
            color = new THREE.Color(0.9, 0.4, 0.2);
        } else if (planetData.temperature > 300) {
            color = planetData.type === 'gas' ? 
                new THREE.Color(0.9, 0.7, 0.3) : 
                new THREE.Color(0.4, 0.7, 0.3);
        } else {
            color = new THREE.Color(0.3, 0.5, 0.8);
        }
    }
    
    return new THREE.MeshBasicMaterial({ 
        color: color
    });
}

function createMoonMesh(moonData) {
    const geometry = new THREE.SphereGeometry(moonData.size, 12, 12);
    const material = new THREE.MeshBasicMaterial({ 
        color: 0x888888
    });
    
    const moon = new THREE.Mesh(geometry, material);
    moon.userData = moonData;
    
    return moon;
}

function createOrbit(radius, inclination, color = 0x444466) {
    const orbitGeometry = new THREE.RingGeometry(radius - 0.1, radius, 32);
    const orbitMaterial = new THREE.MeshBasicMaterial({ 
        color: color,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.3
    });
    const orbit = new THREE.Mesh(orbitGeometry, orbitMaterial);
    orbit.rotation.x = Math.PI / 2;
    orbit.rotation.z = inclination;
    return orbit;
}

// Smooth camera animation function
function animateCameraTo(targetPosition, targetLookAt, duration = 2000, onComplete = null) {
    if (isAnimating) return;
    
    isAnimating = true;
    controls.enabled = false;
    
    const startPosition = camera.position.clone();
    const startLookAt = controls.target.clone();
    const startTime = Date.now();
    
    function updateAnimation() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Smooth easing function
        const easeProgress = progress < 0.5 
            ? 2 * progress * progress 
            : 1 - Math.pow(-2 * progress + 2, 2) / 2;
        
        // Interpolate camera position
        camera.position.lerpVectors(startPosition, targetPosition, easeProgress);
        
        // Interpolate look-at target
        controls.target.lerpVectors(startLookAt, targetLookAt, easeProgress);
        controls.update();
        
        if (progress < 1) {
            animationFrameId = requestAnimationFrame(updateAnimation);
        } else {
            // Animation complete
            isAnimating = false;
            controls.enabled = true;
            if (onComplete) onComplete();
        }
    }
    
    updateAnimation();
}

// Zoom to system with smooth animation
function zoomToSystem(system) {
    console.log("Zooming to system:", system.name);
    
    const systemPosition = system.position.clone();
    const distanceToSystem = systemPosition.length();
    const zoomDistance = Math.max(distanceToSystem * 0.1, 50); // Don't get too close
    
    // Calculate position for system view (approach from an angle)
    const approachVector = systemPosition.clone().normalize();
    const cameraPosition = systemPosition.clone().add(
        approachVector.multiplyScalar(zoomDistance)
    );
    
    // Add some vertical offset for better view
    cameraPosition.y += zoomDistance * 0.3;
    
    updateCameraStatus(`Zooming to ${system.name}`);
    
    animateCameraTo(cameraPosition, systemPosition, 2500, () => {
        // After zooming in, enter the system
        setTimeout(() => enterSystem(system.name), 500);
    });
}

// Zoom to planet with smooth animation
function zoomToPlanet(planetMesh) {
    const planetPosition = planetMesh.position.clone();
    const planetSize = planetMesh.userData.size;
    const zoomDistance = planetSize * 8; // Distance based on planet size
    
    // Calculate position for close planet view
    const cameraPosition = planetPosition.clone();
    cameraPosition.x += zoomDistance;
    cameraPosition.y += zoomDistance * 0.5;
    cameraPosition.z += zoomDistance;
    
    updateCameraStatus(`Viewing ${planetMesh.userData.pl_name}`);
    
    animateCameraTo(cameraPosition, planetPosition, 1500);
}

function updateCameraStatus(status) {
    const cameraStatusElement = document.getElementById('camera-status');
    if (cameraStatusElement) {
        cameraStatusElement.textContent = status;
    }
}

function showSystemInfo(system) {
    navigationPanel.innerHTML = `
        <div class="system-info">
            <h3>${system.name}</h3>
            <div class="system-stats">
                <p><strong>Planets:</strong> ${system.planets.length}</p>
                <p><strong>Star Temperature:</strong> ${system.data.st_teff}K</p>
                <p><strong>Distance:</strong> ${system.data.sy_dist} ly</p>
            </div>
            <button class="enter-btn" data-system="${system.name}">
                Explore System
            </button>
            <button class="zoom-btn" data-system="${system.name}">
                Zoom to System
            </button>
        </div>
    `;
    navigationPanel.style.display = 'block';
    
    // Add event listeners to buttons
    const enterBtn = navigationPanel.querySelector('.enter-btn');
    enterBtn.addEventListener('click', () => {
        enterSystem(system.name);
    });
    
    const zoomBtn = navigationPanel.querySelector('.zoom-btn');
    zoomBtn.addEventListener('click', () => {
        zoomToSystem(system);
    });
}

function showPlanetInfo(planetData) {
    const moonInfo = planetData.moons.length > 0 ? 
        `<p><strong>Moons:</strong> ${planetData.moons.length}</p>` : 
        '<p><strong>Moons:</strong> None</p>';
    
    planetInfoModal.innerHTML = `
        <div class="planet-modal">
            <div class="planet-header">
                <h2>${planetData.pl_name}</h2>
                <div class="planet-badge ${planetData.type}">${planetData.type === 'gas' ? 'Gas Giant' : 'Rocky Planet'}</div>
            </div>
            
            <div class="planet-stats">
                <div class="stat-row">
                    <div class="stat">
                        <label>Radius</label>
                        <span>${planetData.pl_rade} R⊕</span>
                    </div>
                    <div class="stat">
                        <label>Mass</label>
                        <span>${planetData.mass} M⊕</span>
                    </div>
                </div>
                
                <div class="stat-row">
                    <div class="stat">
                        <label>Temperature</label>
                        <span>${planetData.temperature}K</span>
                    </div>
                    <div class="stat">
                        <label>Orbital Period</label>
                        <span>${planetData.pl_orbper} days</span>
                    </div>
                </div>
            </div>
            
            ${moonInfo}
            
            <div class="planet-description">
                <p>${planetData.description}</p>
            </div>
            
            <button class="close-btn">Close</button>
        </div>
    `;
    planetInfoModal.style.display = 'block';
    
    // Add event listener to close button
    const closeBtn = planetInfoModal.querySelector('.close-btn');
    closeBtn.addEventListener('click', () => {
        planetInfoModal.style.display = 'none';
    });
}

function enterSystem(systemName) {
    console.log("Entering system:", systemName);
    
    const system = solarSystems.find(s => s.name === systemName);
    if (!system) {
        console.error("System not found:", systemName);
        return;
    }
    
    currentSolarSystem = system;
    currentView = 'solar-system';
    currentCameraState = CAMERA_STATES.SYSTEM_VIEW;
    
    updateCameraStatus(`Exploring ${systemName}`);
    
    // Clear scene
    while(scene.children.length > 0) { 
        scene.remove(scene.children[0]); 
    }
    
    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0x333333);
    scene.add(ambientLight);
    
    // Add star light
    const starLight = new THREE.PointLight(0xffffff, 1, 1000);
    scene.add(starLight);
    
    // Create new star at center
    const starGeometry = new THREE.SphereGeometry(system.star.geometry.parameters.radius, 16, 16);
    const starMaterial = new THREE.MeshBasicMaterial({ 
        color: system.star.material.color 
    });
    const newStar = new THREE.Mesh(starGeometry, starMaterial);
    newStar.position.set(0, 0, 0);
    scene.add(newStar);
    
    // Add planets and orbits
    system.planets.forEach((planetData, index) => {
        // Create orbit
        const orbit = createOrbit(planetData.orbitRadius, planetData.orbitInclination);
        scene.add(orbit);
        
        // Create planet
        const planet = createPlanetMesh(planetData);
        planet.name = `planet_${index}`;
        
        // Set initial position
        const angle = Math.random() * Math.PI * 2;
        planet.position.x = Math.cos(angle) * planetData.orbitRadius;
        planet.position.z = Math.sin(angle) * planetData.orbitRadius;
        
        scene.add(planet);
        
        // Create moons
        planetData.moons.forEach((moonData, moonIndex) => {
            const moon = createMoonMesh(moonData);
            moon.name = `moon_${index}_${moonIndex}`;
            
            // Set initial moon position
            const moonAngle = Math.random() * Math.PI * 2;
            moon.position.x = planet.position.x + Math.cos(moonAngle) * moonData.orbitRadius;
            moon.position.z = planet.position.z + Math.sin(moonAngle) * moonData.orbitRadius;
            
            scene.add(moon);
            
            // Store moon reference on planet
            if (!planet.userData.moons) planet.userData.moons = [];
            planet.userData.moons.push(moon);
        });
    });
    
    // Position camera with smooth animation
    const systemCameraPosition = new THREE.Vector3(0, 30, 80);
    const systemLookAt = new THREE.Vector3(0, 0, 0);
    
    animateCameraTo(systemCameraPosition, systemLookAt, 1500);
    
    updateNavigationPanel();
    console.log("System loaded:", systemName);
}

function updateSystemsList() {
    let html = `
        <div class="systems-list">
            <h3>Star Systems (${solarSystems.length})</h3>
            <div class="search-box">
                <input type="text" id="system-search" placeholder="Search systems...">
            </div>
            <div class="systems-container">
    `;
    
    solarSystems.forEach((system, index) => {
        const planetCount = system.planets.length;
        const moonCount = system.planets.reduce((total, planet) => total + planet.moons.length, 0);
        
        html += `
            <div class="system-item" data-system="${system.name}">
                <div class="system-header">
                    <span class="system-name">${system.name}</span>
                    <span class="system-distance">${system.data.sy_dist} ly</span>
                </div>
                <div class="system-details">
                    <span class="planets-count">${planetCount} planet${planetCount !== 1 ? 's' : ''}</span>
                    <span class="moons-count">${moonCount} moon${moonCount !== 1 ? 's' : ''}</span>
                </div>
                <button class="system-zoom-btn" data-system="${system.name}">Zoom</button>
            </div>
        `;
    });
    
    html += `
            </div>
        </div>
    `;
    
    systemsListPanel.innerHTML = html;
    
    // Add event listeners to system items
    const systemItems = systemsListPanel.querySelectorAll('.system-item');
    systemItems.forEach(item => {
        item.addEventListener('click', () => {
            const systemName = item.getAttribute('data-system');
            enterSystem(systemName);
        });
    });
    
    // Add event listeners to zoom buttons
    const zoomButtons = systemsListPanel.querySelectorAll('.system-zoom-btn');
    zoomButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent triggering the system item click
            const systemName = btn.getAttribute('data-system');
            const system = solarSystems.find(s => s.name === systemName);
            if (system) {
                zoomToSystem(system);
            }
        });
    });
    
    // Add search functionality
    const searchInput = systemsListPanel.querySelector('#system-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const systemItems = systemsListPanel.querySelectorAll('.system-item');
            
            systemItems.forEach(item => {
                const systemName = item.querySelector('.system-name').textContent.toLowerCase();
                if (systemName.includes(searchTerm)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
}

function updateNavigationPanel() {
    if (currentView === 'galaxy') {
        navigationPanel.innerHTML = `
            <div class="galaxy-view">
                <h3>Galaxy Map</h3>
                <p>${solarSystems.length} star systems discovered</p>
                <p>Click on stars or use the systems list to explore</p>
            </div>
        `;
        navigationPanel.style.display = 'block';
    } else if (currentView === 'solar-system' && currentSolarSystem) {
        let html = `
            <div class="system-view">
                <h3>${currentSolarSystem.name}</h3>
                <div class="planets-list">
        `;
        
        currentSolarSystem.planets.forEach((planet, index) => {
            const moonCount = planet.moons.length;
            html += `
                <div class="planet-item" data-index="${index}">
                    <span class="planet-icon" style="background: ${planet.type === 'gas' ? '#ffaa00' : '#4CAF50'}"></span>
                    <div class="planet-info">
                        <strong>${planet.pl_name}</strong>
                        <span>${planet.description.split(',')[0]} ${moonCount > 0 ? `· ${moonCount} moon${moonCount !== 1 ? 's' : ''}` : ''}</span>
                    </div>
                    <button class="planet-zoom-btn" data-index="${index}">Zoom</button>
                </div>
            `;
        });
        
        html += `
                </div>
                <button class="back-btn">← Back to Galaxy</button>
            </div>
        `;
        navigationPanel.innerHTML = html;
        navigationPanel.style.display = 'block';
        
        // Add event listeners to planet items
        const planetItems = navigationPanel.querySelectorAll('.planet-item');
        planetItems.forEach(item => {
            item.addEventListener('click', () => {
                const planetIndex = parseInt(item.getAttribute('data-index'));
                focusOnPlanet(planetIndex);
            });
        });
        
        // Add event listeners to planet zoom buttons
        const planetZoomButtons = navigationPanel.querySelectorAll('.planet-zoom-btn');
        planetZoomButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevent triggering the planet item click
                const planetIndex = parseInt(btn.getAttribute('data-index'));
                const planetMesh = scene.getObjectByName(`planet_${planetIndex}`);
                if (planetMesh) {
                    zoomToPlanet(planetMesh);
                    showPlanetInfo(currentSolarSystem.planets[planetIndex]);
                }
            });
        });
        
        // Add event listener to back button
        const backBtn = navigationPanel.querySelector('.back-btn');
        backBtn.addEventListener('click', switchToGalaxyView);
    }
}

function focusOnPlanet(planetIndex) {
    if (!currentSolarSystem) return;
    
    const planetData = currentSolarSystem.planets[planetIndex];
    const planetMesh = scene.getObjectByName(`planet_${planetIndex}`);
    
    if (planetMesh) {
        currentCameraState = CAMERA_STATES.PLANET_VIEW;
        
        // Calculate focus position
        const focusPosition = planetMesh.position.clone();
        focusPosition.multiplyScalar(1.5);
        focusPosition.y += 10;
        
        // Animate camera to planet
        animateCameraTo(focusPosition, planetMesh.position, 1200, () => {
            showPlanetInfo(planetData);
        });
    }
}

function switchToGalaxyView() {
    currentView = 'galaxy';
    currentSolarSystem = null;
    currentCameraState = CAMERA_STATES.GALAXY_VIEW;
    
    updateCameraStatus('Galaxy View');
    
    // Clear scene
    while(scene.children.length > 0) { 
        scene.remove(scene.children[0]); 
    }
    
    // Regenerate galaxy
    generateSpiralGalaxy();
    
    // Reset camera with animation
    const galaxyCameraPosition = new THREE.Vector3(0, GALAXY_CONFIG.radius * 0.3, GALAXY_CONFIG.radius * 0.5);
    const galaxyLookAt = new THREE.Vector3(0, 0, 0);
    
    animateCameraTo(galaxyCameraPosition, galaxyLookAt, 1500);
    
    updateNavigationPanel();
    console.log("Returned to galaxy view");
}

function setupEventHandlers() {
    console.log("Setting up event handlers...");
    
    // Mouse move for hover effects
    window.addEventListener('mousemove', (event) => {
        if (isAnimating) return;
        
        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;
        
        if (currentView === 'galaxy') {
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(galaxyStars);
            
            if (intersects.length > 0) {
                const star = intersects[0].object;
                showSystemInfo(star.userData.system);
            } else {
                // Keep navigation panel visible but with galaxy info
                if (navigationPanel.style.display === 'none') {
                    updateNavigationPanel();
                }
            }
        }
    });
    
    // Mouse click for selection
    window.addEventListener('click', (event) => {
        if (isAnimating) return;
        
        if (currentView === 'galaxy') {
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(galaxyStars);
            
            if (intersects.length > 0) {
                const star = intersects[0].object;
                enterSystem(star.userData.system.name);
            }
        } else if (currentView === 'solar-system') {
            // Check if clicked on a planet
            raycaster.setFromCamera(mouse, camera);
            const planetMeshes = [];
            scene.children.forEach(child => {
                if (child.name && child.name.startsWith('planet_')) {
                    planetMeshes.push(child);
                }
            });
            
            const intersects = raycaster.intersectObjects(planetMeshes);
            if (intersects.length > 0) {
                const planet = intersects[0].object;
                const planetIndex = parseInt(planet.name.split('_')[1]);
                focusOnPlanet(planetIndex);
            }
        }
    });
    
    // Keyboard controls
    window.addEventListener('keydown', (event) => {
        if (isAnimating) return;
        
        if (event.key === 'i' || event.key === 'I') {
            if (currentView === 'solar-system') {
                switchToGalaxyView();
            } else if (currentCameraState === CAMERA_STATES.PLANET_VIEW) {
                // Return to system view from planet view
                const systemCameraPosition = new THREE.Vector3(0, 30, 80);
                const systemLookAt = new THREE.Vector3(0, 0, 0);
                animateCameraTo(systemCameraPosition, systemLookAt, 1000);
                currentCameraState = CAMERA_STATES.SYSTEM_VIEW;
                updateCameraStatus(`Exploring ${currentSolarSystem.name}`);
            }
        }
    });
    
    // Window resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    
    console.log("Event handlers setup complete");
}

function animate() {
    requestAnimationFrame(animate);
    
    // Animate planets and moons in solar system view
    if (currentView === 'solar-system' && currentSolarSystem && !isAnimating) {
        const time = Date.now() * 0.001;
        
        currentSolarSystem.planets.forEach((planetData, index) => {
            const planet = scene.getObjectByName(`planet_${index}`);
            if (planet) {
                // Orbital motion
                const angle = time * planetData.revolutionSpeed * 0.1;
                const radius = planetData.orbitRadius * (1 + parseFloat(planetData.pl_orbeccen) * Math.cos(angle));
                
                planet.position.x = Math.cos(angle) * radius;
                planet.position.z = Math.sin(angle) * radius;
                
                // Rotation
                planet.rotation.y += planetData.rotationSpeed;
                
                // Animate moons
                if (planet.userData.moons) {
                    planet.userData.moons.forEach((moon, moonIndex) => {
                        const moonData = planetData.moons[moonIndex];
                        const moonAngle = time * moonData.revolutionSpeed;
                        
                        moon.position.x = planet.position.x + Math.cos(moonAngle) * moonData.orbitRadius;
                        moon.position.z = planet.position.z + Math.sin(moonAngle) * moonData.orbitRadius;
                        moon.rotation.y += moonData.rotationSpeed;
                    });
                }
            }
        });
    }
    
    controls.update();
    renderer.render(scene, camera);
}

// Start the application when the page loads
window.addEventListener('DOMContentLoaded', init);