import re

file_path = "templates/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace SATTVA and Sattva
html = html.replace('SATTVA', 'AYURPULSE')
html = html.replace('Sattva', 'Ayurpulse')

# Make the Holistic Rituals cards clickable
html = html.replace('<!-- Holistic Card 1 -->\n                    <div class="tilt-card interactive-target w-full h-[450px]">',
                    '<!-- Holistic Card 1 -->\n                    <div class="tilt-card interactive-target w-full h-[450px] cursor-pointer" onclick="openAgni()">')

html = html.replace('<!-- Holistic Card 2 -->\n                    <div class="tilt-card interactive-target w-full h-[450px]">',
                    '<!-- Holistic Card 2 -->\n                    <div class="tilt-card interactive-target w-full h-[450px] cursor-pointer" onclick="openRhythm()">')

html = html.replace('<!-- Holistic Card 3 -->\n                    <div class="tilt-card interactive-target w-full h-[450px]">',
                    '<!-- Holistic Card 3 -->\n                    <div class="tilt-card interactive-target w-full h-[450px] cursor-pointer" onclick="openPrana()">')

modals_html = """
    <!-- Custom Modals -->
    <div id="ayur-modals" class="fixed inset-0 z-[99999] hidden flex justify-center items-center pointer-events-none">
        <div class="absolute inset-0 bg-obsidian/90 backdrop-blur-md transition-opacity duration-500 opacity-0" id="modal-bg"></div>
        
        <!-- Agni Modal -->
        <div id="modal-agni" class="glass-panel p-10 rounded-[40px] max-w-lg w-full transform scale-95 opacity-0 transition-all duration-500 hidden z-10 pointer-events-auto">
            <h3 class="font-display italic text-4xl text-primary mb-4">Awaken Agni</h3>
            <p class="text-gray-300 font-sans font-light mb-6">Your digestive fire is the root of your health. Let's kindle it.</p>
            <div class="bg-primary/10 rounded-2xl p-6 border border-primary/20 text-center relative overflow-hidden">
                <div class="absolute inset-0 bg-[url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><circle cx=%2250%22 cy=%2250%22 r=%2240%22 fill=%22none%22 stroke=%22rgba(212,175,55,0.2)%22 stroke-width=%222%22/></svg>')] bg-center bg-no-repeat bg-contain opacity-50 animate-spin-slow"></div>
                <h4 class="text-white font-bold tracking-widest uppercase text-sm mb-2">Current Recommendation</h4>
                <p class="text-primary italic font-display text-xl" id="agni-recommendation">Processing temporal alignment...</p>
            </div>
            <button onclick="closeModals()" class="mt-8 w-full border border-gray-600 hover:border-primary text-gray-400 hover:text-white px-6 py-3 rounded-full transition-all text-xs tracking-widest uppercase">Close</button>
        </div>

        <!-- Rhythm Modal -->
        <div id="modal-rhythm" class="glass-panel p-10 rounded-[40px] max-w-lg w-full transform scale-95 opacity-0 transition-all duration-500 hidden z-10 pointer-events-auto">
            <h3 class="font-display italic text-4xl text-secondary mb-4">Establish Rhythm</h3>
            <p class="text-gray-300 font-sans font-light mb-6">Align your macrocosm with the microcosm of your body.</p>
            <ul class="space-y-4 font-sans text-sm text-gray-400">
                <li class="flex items-center"><span class="w-2 h-2 rounded-full bg-secondary mr-3 shadow-[0_0_10px_#10b981]"></span> <strong>06:00 AM</strong> - Wake up & Tongue Scraping</li>
                <li class="flex items-center"><span class="w-2 h-2 rounded-full bg-secondary mr-3 shadow-[0_0_10px_#10b981]"></span> <strong>07:00 AM</strong> - Yoga & Light Meditation</li>
                <li class="flex items-center"><span class="w-2 h-2 rounded-full bg-secondary mr-3 shadow-[0_0_10px_#10b981]"></span> <strong>12:30 PM</strong> - Largest Meal of the Day</li>
                <li class="flex items-center"><span class="w-2 h-2 rounded-full bg-secondary mr-3 shadow-[0_0_10px_#10b981]"></span> <strong>08:00 PM</strong> - Digital Sunset</li>
                <li class="flex items-center"><span class="w-2 h-2 rounded-full bg-secondary mr-3 shadow-[0_0_10px_#10b981]"></span> <strong>10:00 PM</strong> - Restorative Sleep</li>
            </ul>
            <button onclick="closeModals()" class="mt-8 w-full border border-gray-600 hover:border-secondary text-gray-400 hover:text-white px-6 py-3 rounded-full transition-all text-xs tracking-widest uppercase">Close</button>
        </div>

        <!-- Prana Modal -->
        <div id="modal-prana" class="glass-panel p-10 rounded-[40px] max-w-lg w-full transform scale-95 opacity-0 transition-all duration-500 hidden z-10 pointer-events-auto text-center border-t border-earth/40">
            <h3 class="font-display italic text-4xl text-earth mb-2">Move Prana</h3>
            <p class="text-gray-300 font-sans font-light mb-8 text-sm">Follow the pulsing circle to regulate your nervous system.</p>
            
            <div class="relative w-48 h-48 mx-auto flex items-center justify-center mb-8">
                <div id="prana-circle" class="absolute w-24 h-24 bg-gradient-to-tr from-earth to-primary rounded-full blur-md opacity-50 transition-all duration-[4000ms] ease-in-out"></div>
                <div id="prana-inner" class="absolute w-24 h-24 bg-obsidian rounded-full border border-earth/50 flex items-center justify-center transition-all duration-[4000ms] ease-in-out z-10 shadow-[0_0_30px_rgba(139,90,43,0.3)]">
                    <span id="prana-text" class="text-white font-sans text-xs tracking-widest uppercase">Inhale</span>
                </div>
            </div>

            <button onclick="closeModals()" class="mt-4 w-full border border-gray-600 hover:border-earth text-gray-400 hover:text-white px-6 py-3 rounded-full transition-all text-xs tracking-widest uppercase">End Session</button>
        </div>
    </div>
"""

# Insert Modals before the scripts
html = html.replace('<!-- Scripts for all Interactions -->', modals_html + '\n    <!-- Scripts for all Interactions -->')

# Add JS functions
js_logic = """
        // --- Modal & Ritual Logic ---
        const modalContainer = document.getElementById('ayur-modals');
        const modalBg = document.getElementById('modal-bg');
        let pranaInterval;

        function showModalContainer() {
            modalContainer.classList.remove('hidden');
            setTimeout(() => {
                modalBg.classList.remove('opacity-0');
                modalBg.classList.add('opacity-100');
            }, 10);
        }

        function revealModal(id) {
            const el = document.getElementById(id);
            el.classList.remove('hidden');
            setTimeout(() => {
                el.classList.remove('scale-95', 'opacity-0');
                el.classList.add('scale-100', 'opacity-100');
            }, 50);
        }

        function hideAllModals() {
            ['modal-agni', 'modal-rhythm', 'modal-prana'].forEach(id => {
                const el = document.getElementById(id);
                el.classList.remove('scale-100', 'opacity-100');
                el.classList.add('scale-95', 'opacity-0');
                setTimeout(() => el.classList.add('hidden'), 500);
            });
            clearInterval(pranaInterval);
        }

        function closeModals() {
            hideAllModals();
            modalBg.classList.remove('opacity-100');
            modalBg.classList.add('opacity-0');
            setTimeout(() => {
                modalContainer.classList.add('hidden');
            }, 500);
        }

        window.openAgni = function() {
            showModalContainer();
            revealModal('modal-agni');
            const hour = new Date().getHours();
            const textEl = document.getElementById('agni-recommendation');
            if(hour < 10) textEl.innerText = "Warm water with lemon & ginger.";
            else if(hour < 15) textEl.innerText = "CCF Tea (Cumin, Coriander, Fennel).";
            else if(hour < 20) textEl.innerText = "A pinch of ginger with rock salt.";
            else textEl.innerText = "Triphala to cleanse & rest the gut.";
        };

        window.openRhythm = function() {
            showModalContainer();
            revealModal('modal-rhythm');
        };

        window.openPrana = function() {
            showModalContainer();
            revealModal('modal-prana');
            
            const outer = document.getElementById('prana-circle');
            const inner = document.getElementById('prana-inner');
            const txt = document.getElementById('prana-text');
            
            let phase = 0; // 0: inhale, 1: exhale
            
            // Initial state
            txt.innerText = "Inhale";
            outer.style.transform = "scale(2)";
            inner.style.transform = "scale(1.5)";

            pranaInterval = setInterval(() => {
                phase = 1 - phase;
                if(phase === 1) {
                    txt.innerText = "Exhale";
                    outer.style.transform = "scale(1)";
                    inner.style.transform = "scale(1)";
                } else {
                    txt.innerText = "Inhale";
                    outer.style.transform = "scale(2)";
                    inner.style.transform = "scale(1.5)";
                }
            }, 4000);
        };
        
        // Custom animation for spin slow
        const styleSheet = document.createElement("style");
        styleSheet.innerText = `
            @keyframes spin-slow { 100% { transform: rotate(360deg); } }
            .animate-spin-slow { animation: spin-slow 8s linear infinite; }
        `;
        document.head.appendChild(styleSheet);
"""

html = html.replace('// --- 1. Preloader & Init ---', js_logic + '\n        // --- 1. Preloader & Init ---')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
