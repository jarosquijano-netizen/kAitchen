// API helper functions
const API = {
    async request(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            
            // Parse JSON even for error status codes
            const data = await response.json();
            
            // If response is not ok, throw error with data
            if (!response.ok) {
                const error = new Error(data.error || `HTTP ${response.status}`);
                error.status = response.status;
                error.data = data;
                throw error;
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    get(url) {
        return this.request(url);
    },

    post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    delete(url) {
        return this.request(url, {
            method: 'DELETE'
        });
    }
};

// Alert functions
function showAlert(message, type = 'success') {
    const alertsContainer = document.getElementById('alerts');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} show`;
    alert.textContent = message;
    
    alertsContainer.appendChild(alert);
    
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        
        // Update active tab
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Show corresponding content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        // Load data for the tab
        if (tabName === 'family') {
            loadFamilyProfiles();
        } else if (tabName === 'recipes') {
            loadRecipes();
        } else if (tabName === 'menu') {
            // Check if we're viewing current week or another week
            const calculatedCurrentWeek = getCurrentWeekStart();
            const isViewingCurrentWeek = currentViewingWeek && currentViewingWeek === calculatedCurrentWeek;
            
            if (isViewingCurrentWeek) {
                // Reset to current day when viewing current week
                const today = new Date();
                const dayOfWeek = today.getDay();
                const dayMap = [6, 0, 1, 2, 3, 4, 5]; // Sunday=6, Monday=0, etc.
                const currentDayIndex = dayMap[dayOfWeek];
                window.selectedDayIndex = currentDayIndex >= 0 ? currentDayIndex : 0;
                console.log('[TabSwitch] Viewing current week, setting selectedDayIndex to current day:', window.selectedDayIndex);
            } else {
                // Reset to Monday when viewing other weeks
                window.selectedDayIndex = 0;
                console.log('[TabSwitch] Viewing other week, setting selectedDayIndex to Monday (0)');
            }
            loadCurrentWeekMenu();
        } else if (tabName === 'shopping') {
            console.log('[TabSwitch] Loading shopping lists...');
            // Initialize shopping week navigation
            if (!currentShoppingWeek) {
                currentShoppingWeek = getCurrentWeekStart();
            }
            updateShoppingWeekNavigation();
            loadShoppingLists(currentShoppingWeek);
        } else if (tabName === 'settings') {
            loadSettings();
            loadMenuPreferences();
        }
    });
});

// Adult profile functions
function showAdultForm() {
    document.getElementById('adult-form').style.display = 'block';
}

function hideAdultForm() {
    document.getElementById('adult-form').style.display = 'none';
    document.getElementById('adultForm').reset();
}

document.getElementById('adultForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const result = await API.post('/api/adults', data);
        if (result.success) {
            showAlert('Perfil de adulto añadido correctamente', 'success');
            hideAdultForm();
            loadAdults();
        }
    } catch (error) {
        showAlert('Error al guardar el perfil', 'error');
    }
});

async function loadAdults() {
    try {
        console.log('[LoadAdults] Starting to load adults...');
        const result = await API.get('/api/adults');
        console.log('[LoadAdults] API response:', result);
        const container = document.getElementById('adults-list');
        
        if (!container) {
            console.error('[LoadAdults] Container #adults-list not found!');
            return;
        }
        
        if (result.data.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                              d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                    </svg>
                    <h3>No hay perfiles de adultos</h3>
                    <p>Añade el primer perfil para comenzar</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = '<div class="profile-list"></div>';
        const list = container.querySelector('.profile-list');
        
        result.data.forEach(adult => {
            const div = document.createElement('div');
            div.className = 'profile-item';
            
            let badges = '';
            if (adult.alergias) badges += `<span class="badge badge-warning">⚠️ Alergias</span>`;
            if (adult.intolerancias) badges += `<span class="badge badge-warning">⚠️ Intolerancias</span>`;
            if (adult.estilo_alimentacion) badges += `<span class="badge badge-info">${adult.estilo_alimentacion}</span>`;
            
            div.innerHTML = `
                <div class="profile-info">
                    <h3>${adult.nombre} (${adult.edad || 'N/A'} años)</h3>
                    <p>${badges}</p>
                    ${adult.objetivo_alimentario ? `<p>Objetivo: ${adult.objetivo_alimentario}</p>` : ''}
                </div>
                <div class="profile-actions">
                    <button class="btn btn-danger btn-sm" onclick="deleteAdult(${adult.id})">Eliminar</button>
                </div>
            `;
            
            list.appendChild(div);
        });
        
        console.log('[LoadAdults] Successfully loaded', result.data.length, 'adults');
    } catch (error) {
        console.error('[LoadAdults] Error loading adults:', error);
        const container = document.getElementById('adults-list');
        if (container) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>Error al cargar perfiles</h3>
                    <p style="margin-top: 1rem; color: var(--silver);">
                        ${error.message || 'Error desconocido'}
                    </p>
                    <button class="btn btn-primary" onclick="loadAdults()" style="margin-top: 1.5rem;">
                        Reintentar
                    </button>
                </div>
            `;
        }
    }
}

async function deleteAdult(id) {
    if (!confirm('¿Estás seguro de eliminar este perfil?')) return;
    
    try {
        const result = await API.delete(`/api/adults/${id}`);
        if (result.success) {
            showAlert('Perfil eliminado correctamente', 'success');
            loadAdults();
        }
    } catch (error) {
        showAlert('Error al eliminar el perfil', 'error');
    }
}

// Child profile functions
function showChildForm() {
    document.getElementById('child-form').style.display = 'block';
}

function hideChildForm() {
    document.getElementById('child-form').style.display = 'none';
    document.getElementById('childForm').reset();
}

document.getElementById('childForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const result = await API.post('/api/children', data);
        if (result.success) {
            showAlert('Perfil de niño/a añadido correctamente', 'success');
            hideChildForm();
            loadChildren();
        }
    } catch (error) {
        showAlert('Error al guardar el perfil', 'error');
    }
});

async function loadChildren() {
    try {
        console.log('[LoadChildren] Starting to load children...');
        const result = await API.get('/api/children');
        console.log('[LoadChildren] API response:', result);
        const container = document.getElementById('children-list');
        
        if (!container) {
            console.error('[LoadChildren] Container #children-list not found!');
            return;
        }
        
        if (result.data.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                              d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <h3>No hay perfiles de niños</h3>
                    <p>Añade el primer perfil para comenzar</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = '<div class="profile-list"></div>';
        const list = container.querySelector('.profile-list');
        
        result.data.forEach(child => {
            const div = document.createElement('div');
            div.className = 'profile-item';
            
            let badges = '';
            if (child.alergias) badges += `<span class="badge badge-warning">⚠️ Alergias</span>`;
            if (child.intolerancias) badges += `<span class="badge badge-warning">⚠️ Intolerancias</span>`;
            if (child.nivel_exigencia) badges += `<span class="badge badge-info">${child.nivel_exigencia}</span>`;
            
            div.innerHTML = `
                <div class="profile-info">
                    <h3>${child.nombre} (${child.edad} años)</h3>
                    <p>${badges}</p>
                    ${child.acepta_comida_nueva ? `<p>Comida nueva: ${child.acepta_comida_nueva}</p>` : ''}
                </div>
                <div class="profile-actions">
                    <button class="btn btn-danger btn-sm" onclick="deleteChild(${child.id})">Eliminar</button>
                </div>
            `;
            
            list.appendChild(div);
        });
        
        console.log('[LoadChildren] Successfully loaded', result.data.length, 'children');
    } catch (error) {
        console.error('[LoadChildren] Error loading children:', error);
        const container = document.getElementById('children-list');
        if (container) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>Error al cargar perfiles</h3>
                    <p style="margin-top: 1rem; color: var(--silver);">
                        ${error.message || 'Error desconocido'}
                    </p>
                    <button class="btn btn-primary" onclick="loadChildren()" style="margin-top: 1.5rem;">
                        Reintentar
                    </button>
                </div>
            `;
        }
    }
}

async function deleteChild(id) {
    if (!confirm('¿Estás seguro de eliminar este perfil?')) return;
    
    try {
        const result = await API.delete(`/api/children/${id}`);
        if (result.success) {
            showAlert('Perfil eliminado correctamente', 'success');
            loadChildren();
        }
    } catch (error) {
        showAlert('Error al eliminar el perfil', 'error');
    }
}

function loadFamilyProfiles() {
    loadAdults();
    loadChildren();
}

// Recipe functions
function showBatchExtract() {
    document.getElementById('batch-extract').style.display = 'block';
}

function hideBatchExtract() {
    document.getElementById('batch-extract').style.display = 'none';
    document.getElementById('batchUrls').value = '';
}

async function extractRecipe() {
    const url = document.getElementById('recipeUrl').value.trim();
    
    if (!url) {
        showAlert('Por favor, introduce una URL', 'error');
        return;
    }
    
    try {
        showAlert('Extrayendo receta...', 'success');
        const result = await API.post('/api/recipes/extract', { url });
        
        if (result.success) {
            showAlert('Receta extraída correctamente', 'success');
            document.getElementById('recipeUrl').value = '';
            loadRecipes();
        } else {
            showAlert(result.error || 'Error al extraer la receta', 'error');
        }
    } catch (error) {
        showAlert('Error al extraer la receta', 'error');
    }
}

async function extractBatchRecipes() {
    const urlsText = document.getElementById('batchUrls').value.trim();
    
    if (!urlsText) {
        showAlert('Por favor, introduce al menos una URL', 'error');
        return;
    }
    
    const urls = urlsText.split('\n').map(u => u.trim()).filter(u => u);
    
    try {
        showAlert(`Extrayendo ${urls.length} recetas...`, 'success');
        const result = await API.post('/api/recipes/batch', { urls });
        
        if (result.success) {
            showAlert(result.message, 'success');
            hideBatchExtract();
            loadRecipes();
        }
    } catch (error) {
        showAlert('Error al extraer las recetas', 'error');
    }
}

async function deleteRecipe(recipeId, recipeTitle) {
    if (!confirm(`¿Estás seguro de que quieres eliminar "${recipeTitle}"?\n\nEsta acción no se puede deshacer.`)) {
        return;
    }
    
    try {
        const result = await API.delete(`/api/recipes/${recipeId}`);
        
        if (result && result.success) {
            showAlert('Receta eliminada correctamente', 'success');
            loadRecipes(); // Reload the list
        } else {
            const errorMsg = result?.error || 'Error al eliminar la receta';
            showAlert(errorMsg, 'error');
        }
    } catch (error) {
        // Handle JSON parse errors
        if (error.message && error.message.includes('JSON')) {
            showAlert('Error: El servidor no respondió correctamente. Verifica que el servidor esté corriendo.', 'error');
        } else {
            showAlert('Error al eliminar la receta: ' + (error.message || 'Error desconocido'), 'error');
        }
        console.error('Delete recipe error:', error);
    }
}

async function loadRecipes() {
    const container = document.getElementById('recipes-list');
    
    if (!container) {
        console.error('Container recipes-list no encontrado');
        return;
    }
    
    // Show loading state
    container.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--silver);">Cargando recetas...</div>';
    
    try {
        const result = await API.get('/api/recipes');
        
        if (!result || !result.success) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>Error al cargar recetas</h3>
                    <p>${result?.error || 'Error desconocido'}</p>
                    <button class="btn btn-primary" onclick="loadRecipes()" style="margin-top: 16px;">🔄 Reintentar</button>
                </div>
            `;
            return;
        }
        
        if (!result.data || result.data.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                              d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                    </svg>
                    <h3>No hay recetas guardadas</h3>
                    <p>Extrae recetas desde URLs para comenzar</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = '<h3 style="margin-bottom: 16px; font-family: \'Playfair Display\', serif; color: var(--white);">Recetas Guardadas</h3><div class="profile-list"></div>';
        const list = container.querySelector('.profile-list');
        
        result.data.forEach(recipe => {
            const div = document.createElement('div');
            div.className = 'profile-item';
            
            const ingredientsCount = recipe.ingredients ? recipe.ingredients.length : 0;
            const timeInfo = recipe.prep_time ? `${recipe.prep_time} min` : 'N/A';
            
            // Get images and videos from extracted_data
            let images = [];
            let videos = [];
            let videoUrl = null;
            
            if (recipe.extracted_data) {
                try {
                    const extracted = typeof recipe.extracted_data === 'string' 
                        ? JSON.parse(recipe.extracted_data) 
                        : recipe.extracted_data;
                    images = extracted.images || [];
                    videos = extracted.videos || [];
                    videoUrl = extracted.video_url || null;
                } catch (e) {
                    console.error('Error parsing extracted_data:', e);
                }
            }
            
            // Use primary image_url if available
            const primaryImage = recipe.image_url || (images.length > 0 ? images[0] : null);
            
            div.innerHTML = `
                <div class="profile-info" style="display: flex; gap: 12px; align-items: flex-start;">
                    ${primaryImage ? `
                        <div style="flex-shrink: 0; width: 80px; height: 80px; border-radius: 6px; overflow: hidden; background: rgba(255, 255, 255, 0.03); border: 2px solid rgba(255, 255, 255, 0.1); box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                            <img src="${primaryImage}" 
                                 alt="${recipe.title}" 
                                 style="width: 100%; height: 100%; object-fit: cover; cursor: pointer; transition: transform 0.2s;"
                                 onclick="window.open('${primaryImage}', '_blank')"
                                 onerror="this.parentElement.style.display='none'"
                                 onmouseover="this.style.transform='scale(1.05)'"
                                 onmouseout="this.style.transform='scale(1)'"
                                 title="Click para ver imagen completa">
                        </div>
                    ` : `
                        <div style="flex-shrink: 0; width: 80px; height: 80px; border-radius: 6px; background: rgba(255, 255, 255, 0.03); border: 2px solid rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: center; color: var(--silver); font-size: 2rem;">
                            🍳
                        </div>
                    `}
                    <div style="flex: 1; min-width: 0;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                            <h3 style="margin: 0; flex: 1; font-family: 'Playfair Display', serif; color: var(--white);">${recipe.title || 'Sin título'}</h3>
                            <button onclick="deleteRecipe(${recipe.id}, '${(recipe.title || 'esta receta').replace(/'/g, "\\'")}')" 
                                    class="btn btn-danger btn-sm" 
                                    style="margin-left: 12px; padding: 4px 12px; font-size: 0.85rem;"
                                    title="Eliminar receta">
                                🗑️ Eliminar
                            </button>
                        </div>
                        <p style="margin-bottom: 6px;">
                            ${recipe.cuisine_type ? `<span class="badge badge-info">${recipe.cuisine_type}</span>` : ''}
                            <span style="color: var(--silver); margin-left: 8px; font-size: 0.9rem;">
                                ${ingredientsCount} ingredientes • ${timeInfo}
                            </span>
                        </p>
                        ${images.length > 1 ? `
                            <p style="font-size: 0.85rem; color: var(--silver); margin: 4px 0;">
                                📷 ${images.length} imágenes disponibles
                            </p>
                        ` : ''}
                        ${videoUrl || videos.length > 0 ? `
                            <p style="font-size: 0.85rem; color: var(--gold); margin: 4px 0;">
                                🎥 ${videoUrl ? '<a href="' + videoUrl + '" target="_blank" style="color: var(--gold); text-decoration: none;">Ver video</a>' : videos.length + ' videos disponibles'}
                            </p>
                        ` : ''}
                        ${recipe.url ? `<p style="font-size: 0.85rem; color: var(--silver); margin: 4px 0;">
                            <a href="${recipe.url}" target="_blank" style="color: var(--gold); text-decoration: none;">🔗 Ver receta original</a>
                        </p>` : ''}
                    </div>
                </div>
            `;
            
            list.appendChild(div);
        });
        
        // Show success message if recipes loaded
        console.log(`✅ ${result.data.length} recetas cargadas correctamente`);
        
    } catch (error) {
        console.error('Error loading recipes:', error);
        container.innerHTML = `
            <div class="empty-state" style="border: 2px solid rgba(239, 68, 68, 0.5); padding: 24px; border-radius: 12px;">
                <h3 style="color: #FCA5A5;">❌ Error al conectar con el servidor</h3>
                <p style="margin: 16px 0; color: var(--silver);">El servidor no está respondiendo. Verifica que esté corriendo.</p>
                <p style="color: var(--silver); font-size: 0.9rem; margin-bottom: 16px;">
                    Error: ${error.message || 'No se pudo conectar al servidor'}
                </p>
                <div style="display: flex; gap: 10px; justify-content: center;">
                    <button class="btn btn-primary" onclick="loadRecipes()">🔄 Reintentar</button>
                    <button class="btn btn-danger" onclick="location.reload()">🔄 Recargar página</button>
                </div>
                <p style="margin-top: 16px; font-size: 0.85rem; color: var(--silver);">
                    💡 Asegúrate de que el servidor esté corriendo ejecutando: <code style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">python app.py</code>
                </p>
            </div>
        `;
    }
}

// Week navigation state
let currentWeekStart = null;
let currentViewingWeek = null;

// Helper function to get Monday of a given date
function getMondayOfWeek(date) {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0); // Reset time to avoid timezone issues
    const day = d.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
    // Calculate days to subtract to get to Monday
    // JavaScript getDay(): 0=Sunday, 1=Monday, 2=Tuesday, ..., 6=Saturday
    // To get to Monday:
    // - If Sunday (0), go back 6 days
    // - If Monday (1), go back 0 days
    // - If Tuesday (2), go back 1 day
    // - If Wednesday (3), go back 2 days
    // - If Thursday (4), go back 3 days
    // - If Friday (5), go back 4 days
    // - If Saturday (6), go back 5 days
    let diff;
    if (day === 0) {
        diff = -6; // Sunday -> go back 6 days to Monday
    } else {
        diff = -(day - 1); // Monday=0, Tuesday=-1, Wednesday=-2, etc.
    }
    const monday = new Date(d);
    monday.setDate(d.getDate() + diff);
    
    // Format dates using local components to avoid timezone issues
    const formatLocalDate = (date) => {
        const y = date.getFullYear();
        const m = date.getMonth();
        const day = date.getDate();
        return `${y}-${String(m + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    };
    
    // Debug log
    const dayNames = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    console.log('[getMondayOfWeek] Input date:', formatLocalDate(d), `(${dayNames[day]})`, 'diff:', diff, '-> Monday:', formatLocalDate(monday));
    
    // Return a new Date object with the correct local date components to avoid timezone issues
    const mondayYear = monday.getFullYear();
    const mondayMonth = monday.getMonth();
    const mondayDate = monday.getDate();
    return new Date(mondayYear, mondayMonth, mondayDate, 0, 0, 0, 0);
}

// Toggle sidebar collapse/expand
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.style.transform = sidebar.style.transform === 'translateX(-100%)' ? 'translateX(0)' : 'translateX(-100%)';
    }
}

// Helper function to format week start date
function formatWeekStart(date) {
    const d = new Date(date);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return d.toLocaleDateString('es-ES', options);
}

// Helper function to get current week start (Monday)
function getCurrentWeekStart() {
    // Use local date components to avoid timezone conversion issues
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const date = today.getDate();
    
    // Create date using local components (avoids UTC conversion)
    const localToday = new Date(year, month, date, 0, 0, 0, 0);
    
    // Log the actual date and day
    const dayNames = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    const todayStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;
    const todayDay = localToday.getDay();
    console.log('[getCurrentWeekStart] Local date:', todayStr, `(${dayNames[todayDay]})`);
    
    const monday = getMondayOfWeek(localToday);
    // Format Monday using local components to avoid timezone issues
    const mondayYear = monday.getFullYear();
    const mondayMonth = monday.getMonth();
    const mondayDate = monday.getDate();
    const result = `${mondayYear}-${String(mondayMonth + 1).padStart(2, '0')}-${String(mondayDate).padStart(2, '0')}`;
    console.log('[getCurrentWeekStart] Calculated Monday:', result);
    return result;
}

// Helper function to get next week start (Monday)
function getNextWeekStart() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const currentMonday = getMondayOfWeek(today);
    const nextMonday = new Date(currentMonday);
    nextMonday.setDate(currentMonday.getDate() + 7);
    const result = nextMonday.toISOString().split('T')[0];
    console.log('[getNextWeekStart] Today:', today.toISOString().split('T')[0]);
    console.log('[getNextWeekStart] Current Monday:', currentMonday.toISOString().split('T')[0]);
    console.log('[getNextWeekStart] Next Monday:', result);
    return result;
}

// Menu generation - generates for the currently viewing week
async function generateMenu() {
    const loading = document.getElementById('menu-loading');
    const display = document.getElementById('menu-display');
    
    loading.classList.add('show');
    display.innerHTML = '';
    
    // Use currentViewingWeek if available, otherwise use selector
    let weekStartDate = null;
    
    // Always calculate fresh to ensure we're using the correct current week
    const calculatedCurrentWeek = getCurrentWeekStart();
    console.log('[GenerateMenu] Calculated current week:', calculatedCurrentWeek);
    console.log('[GenerateMenu] currentViewingWeek:', currentViewingWeek);
    
    if (currentViewingWeek && currentViewingWeek !== calculatedCurrentWeek) {
        // If currentViewingWeek is set but different from calculated current week,
        // use currentViewingWeek (user is viewing a different week)
        weekStartDate = currentViewingWeek;
        console.log('[GenerateMenu] Using currentViewingWeek (different week):', weekStartDate);
    } else {
        // Use calculated current week (most accurate)
        weekStartDate = calculatedCurrentWeek;
        currentViewingWeek = calculatedCurrentWeek;
        console.log('[GenerateMenu] Using calculated current week:', weekStartDate);
        updateWeekNavigation();
    }
    
    // Create AbortController for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 360000); // 6 minutes timeout
    
    try {
        console.log('[Frontend] Iniciando generación de menú para semana:', weekStartDate);
        
        // Use fetch directly with timeout
        const response = await fetch('/api/menu/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                week_start_date: weekStartDate
            }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        const result = await response.json();
        
        loading.classList.remove('show');
        
        if (!response.ok) {
            throw { status: response.status, data: result };
        }
        
        if (result.success) {
            console.log('[Frontend] Menú generado correctamente');
            console.log('[Frontend] Result structure:', result);
            console.log('[Frontend] week_start from response:', result.week_start);
            const weekDate = formatWeekStart(currentViewingWeek);
            showAlert(`Menú generado correctamente para ${weekDate}`, 'success');
            
            // Update current viewing week - use week_start from response if available
            if (result.week_start) {
                currentViewingWeek = result.week_start;
                console.log('[GenerateMenu] Set currentViewingWeek to:', currentViewingWeek, 'from API response week_start');
            } else {
                currentViewingWeek = weekStartDate;
                console.log('[GenerateMenu] Set currentViewingWeek to:', currentViewingWeek, 'from request (no week_start in response)');
            }
            updateWeekNavigation();
            // Update button to show "Regenerar" since menu now exists
            updateGenerateButtonForWeek(currentViewingWeek);
            
            // Display menu directly on screen - check both possible response structures
            let menuData = result.menu || result.data?.menu_data || result.data?.menu;
            
            // If menuData is a string (JSON string), parse it
            if (typeof menuData === 'string') {
                try {
                    menuData = JSON.parse(menuData);
                    console.log('[Frontend] Parsed menu data from string');
                } catch (e) {
                    console.error('[Frontend] Failed to parse menu data string:', e);
                }
            }
            
            console.log('[Frontend] Menu data extracted:', menuData ? 'Found' : 'Not found');
            console.log('[Frontend] Menu data type:', typeof menuData);
            console.log('[Frontend] Menu data keys:', menuData ? Object.keys(menuData) : 'N/A');
            
            // Check if menuData is a single meal instead of full menu structure
            if (menuData && menuData.nombre && menuData.ingredientes && !menuData.menu_adultos && !menuData.menu_ninos && !menuData.dias && !menuData.semana) {
                console.warn('[Frontend] Menu data appears to be a single meal, checking raw_response for full menu...');
                
                // Try to extract from raw_response if available
                if (result.raw_response) {
                    try {
                        // Try to parse raw_response as JSON (it might already be JSON string)
                        let rawMenu;
                        if (typeof result.raw_response === 'string') {
                            // Try direct parse first
                            try {
                                rawMenu = JSON.parse(result.raw_response);
                            } catch (e) {
                                // Try to extract JSON from markdown code block
                                const jsonMatch = result.raw_response.match(/```json\s*([\s\S]*?)\s*```/);
                                if (jsonMatch) {
                                    rawMenu = JSON.parse(jsonMatch[1]);
                                } else {
                                    // Try to find JSON object in the string
                                    const jsonObjectMatch = result.raw_response.match(/\{[\s\S]*\}/);
                                    if (jsonObjectMatch) {
                                        rawMenu = JSON.parse(jsonObjectMatch[0]);
                                    } else {
                                        throw new Error('No JSON found in raw_response');
                                    }
                                }
                            }
                        } else {
                            rawMenu = result.raw_response;
                        }
                        
                        console.log('[Frontend] Parsed raw_response, keys:', Object.keys(rawMenu));
                        
                        // Check if rawMenu has the correct structure
                        if (rawMenu.menu_adultos || rawMenu.menu_ninos || rawMenu.dias || rawMenu.semana) {
                            menuData = rawMenu;
                            console.log('[Frontend] Using full menu structure from raw_response');
                        } else {
                            console.warn('[Frontend] raw_response also doesn\'t have expected structure');
                        }
                    } catch (e) {
                        console.error('[Frontend] Failed to parse raw_response:', e);
                    }
                }
            }
            
            if (menuData) {
                window.currentMenuData = menuData; // Store for potential future use
                console.log('[Frontend] Final menu data keys:', Object.keys(menuData));
                console.log('[Frontend] Calling displayMenu');
                displayMenu(menuData);
                
                // After displaying menu, reload it from the database to ensure consistency
                // This ensures we're displaying the menu with the correct week_start_date
                setTimeout(async () => {
                    try {
                        console.log('[GenerateMenu] Reloading menu from database for week:', currentViewingWeek);
                        const response = await fetch(`/api/menu/week/${currentViewingWeek}`);
                        if (response.ok) {
                            const reloadResult = await response.json();
                            if (reloadResult.success && reloadResult.data) {
                                const reloadedMenuData = reloadResult.data.menu_data;
                                if (reloadedMenuData) {
                                    console.log('[GenerateMenu] Menu reloaded successfully, updating display');
                                    displayMenu(reloadedMenuData);
                                }
                            }
                        }
                    } catch (error) {
                        console.warn('[GenerateMenu] Could not reload menu from database:', error);
                        // Menu is already displayed, so this is not critical
                    }
                }, 500); // Small delay to ensure menu is saved
                
                // Reload shopping list if we're on the shopping tab
                const activeTab = document.querySelector('.tab.active');
                if (activeTab && activeTab.getAttribute('data-tab') === 'shopping') {
                    console.log('[Frontend] Shopping tab is active, reloading shopping list...');
                    setTimeout(() => {
                        loadShoppingList();
                    }, 1000); // Delay to ensure menu is saved to database
                }
            } else {
                console.warn('[Frontend] No menu data found in result');
                console.warn('[Frontend] Result keys:', Object.keys(result));
                // Show error message
                display.innerHTML = `
                    <div class="empty-state">
                        <h3>Error: No se encontraron datos del menú</h3>
                        <p style="margin-top: 1rem; color: var(--silver);">
                            El menú se generó pero no se pudo extraer la información. Revisa la consola (F12) para más detalles.
                        </p>
                    </div>
                `;
            }
        } else {
            // Show detailed error message
            const errorMsg = result.error || 'Error al generar el menú';
            const message = result.message || '';
            showAlert(errorMsg + (message ? ': ' + message : ''), 'error');
            
            // Show error in display area
            display.innerHTML = `
                <div class="empty-state">
                    <h3>Error al generar el menú</h3>
                    <p style="margin-top: 1rem; color: var(--silver);">
                        ${errorMsg}
                    </p>
                    ${message ? `<p style="margin-top: 0.5rem; color: var(--silver); font-size: 0.9rem;">${message}</p>` : ''}
                    ${errorMsg.includes('perfil') ? `
                        <p style="margin-top: 1rem; color: var(--gold);">
                            💡 Ve a la pestaña "Family" y añade al menos un perfil de adulto o niño.
                        </p>
                    ` : ''}
                    ${errorMsg.includes('API') || errorMsg.includes('API key') || errorMsg.includes('Anthropic') ? `
                        <p style="margin-top: 1rem; color: var(--gold);">
                            💡 Ve a la pestaña "Settings" y configura tu API key de Anthropic.
                        </p>
                    ` : ''}
                    ${errorMsg.includes('Timeout') || errorMsg.includes('timeout') ? `
                        <p style="margin-top: 1rem; color: var(--gold);">
                            💡 La generación tardó demasiado. Intenta de nuevo o verifica tu conexión a internet.
                        </p>
                    ` : ''}
                    <button class="btn btn-primary" onclick="generateMenu()" style="margin-top: 1.5rem;">
                        Reintentar
                    </button>
                </div>
            `;
        }
    } catch (error) {
        clearTimeout(timeoutId);
        loading.classList.remove('show');
        
        // Check if it's a timeout/abort
        if (error.name === 'AbortError' || error.message?.includes('aborted')) {
            const errorMsg = 'Timeout: La generación del menú tardó demasiado tiempo (>6 minutos). Intenta de nuevo.';
            showAlert(errorMsg, 'error');
            display.innerHTML = `
                <div class="empty-state">
                    <h3>Timeout al generar el menú</h3>
                    <p style="margin-top: 1rem; color: var(--silver);">
                        La generación del menú está tardando demasiado tiempo. Esto puede deberse a:
                    </p>
                    <ul style="margin-top: 1rem; color: var(--silver); text-align: left; max-width: 600px; margin-left: auto; margin-right: auto;">
                        <li>Muchas recetas en la base de datos</li>
                        <li>Perfiles familiares muy detallados</li>
                        <li>Problemas de conexión con la API de Anthropic</li>
                    </ul>
                    <p style="margin-top: 1.5rem; color: var(--gold);">
                        💡 Intenta de nuevo. Si el problema persiste, verifica tu conexión a internet y la API key.
                    </p>
                    <button class="btn btn-primary" onclick="generateMenu()" style="margin-top: 1.5rem;">
                        Reintentar
                    </button>
                </div>
            `;
        } else {
            // Extract error message
            const errorMsg = error.data?.error || error.message || 'Error desconocido';
            showAlert('Error al generar el menú: ' + errorMsg, 'error');
            
            // Show detailed error in display area
            display.innerHTML = `
                <div class="empty-state">
                    <h3>Error al generar el menú</h3>
                    <p style="margin-top: 1rem; color: var(--silver);">
                        ${errorMsg}
                    </p>
                    ${errorMsg.includes('perfil') || error.status === 400 ? `
                        <p style="margin-top: 1rem; color: var(--gold);">
                            💡 Asegúrate de tener al menos un perfil familiar añadido y la API key configurada.
                        </p>
                    ` : ''}
                    <button class="btn btn-primary" onclick="generateMenu()" style="margin-top: 1.5rem;">
                        Reintentar
                    </button>
                </div>
            `;
        }
        
        console.error('Menu generation error:', error);
    }
}

// Regenerate individual menu for current day only
async function regenerateIndividualMenu() {
    const loading = document.getElementById('menu-loading');
    const display = document.getElementById('menu-display');
    
    // Check if there's a current menu and selected day
    if (!window.currentMenuDataForDays || window.selectedDayIndex === undefined) {
        showAlert('Por favor, primero genera o carga un menú semanal completo', 'warning');
        return;
    }
    
    const currentDayIndex = window.selectedDayIndex;
    const dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
    const currentDay = dias[currentDayIndex];
    
    if (!currentDay) {
        showAlert('Día no válido seleccionado', 'error');
        return;
    }
    
    loading.classList.add('show');
    
    try {
        console.log(`[RegenerateDay] Regenerating menu for day: ${currentDay} (index: ${currentDayIndex})`);
        
        const response = await fetch('/api/menu/regenerate-day', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                week_start_date: currentViewingWeek || getCurrentWeekStart(),
                day_index: currentDayIndex,
                day_name: currentDay,
                current_menu_data: window.currentMenuDataForDays
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`Menú del día ${currentDay.charAt(0).toUpperCase() + currentDay.slice(1)} regenerado exitosamente`, 'success');
            
            // Update the menu data with the regenerated day
            if (result.data && result.data.menu_data) {
                // Merge the regenerated day into the existing menu data
                const updatedMenuData = { ...window.currentMenuDataForDays };
                
                // Update both adults and children menus if they exist
                if (result.data.menu_data.menu_adultos && result.data.menu_data.menu_adultos.dias && result.data.menu_data.menu_adultos.dias[currentDay]) {
                    if (!updatedMenuData.menu_adultos) updatedMenuData.menu_adultos = { dias: {} };
                    if (!updatedMenuData.menu_adultos.dias) updatedMenuData.menu_adultos.dias = {};
                    updatedMenuData.menu_adultos.dias[currentDay] = result.data.menu_data.menu_adultos.dias[currentDay];
                }
                
                if (result.data.menu_data.menu_ninos && result.data.menu_data.menu_ninos.dias && result.data.menu_data.menu_ninos.dias[currentDay]) {
                    if (!updatedMenuData.menu_ninos) updatedMenuData.menu_ninos = { dias: {} };
                    if (!updatedMenuData.menu_ninos.dias) updatedMenuData.menu_ninos.dias = {};
                    updatedMenuData.menu_ninos.dias[currentDay] = result.data.menu_data.menu_ninos.dias[currentDay];
                }
                
                // Update global menu data and re-render
                window.currentMenuDataForDays = updatedMenuData;
                
                // Re-render the menu to show the updated day
                displayMenu(updatedMenuData);
            }
        } else {
            showAlert('Error al regenerar el menú del día: ' + (result.error || 'Error desconocido'), 'error');
        }
    } catch (error) {
        console.error('Error regenerating individual menu:', error);
        showAlert('Error al regenerar el menú del día: ' + (error.message || 'Error de conexión'), 'error');
    } finally {
        loading.classList.remove('show');
    }
}

// Regenerate individual meal for specific day and meal type
async function regenerateIndividualMeal(mealType, dayIndex) {
    const loading = document.getElementById('menu-loading');
    
    // Check if there's a current menu and selected day
    if (!window.currentMenuDataForDays || window.selectedDayIndex === undefined) {
        showAlert('Por favor, primero genera o carga un menú semanal completo', 'warning');
        return;
    }
    
    const dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
    const currentDay = dias[dayIndex];
    
    if (!currentDay || !mealType) {
        showAlert('Parámetros inválidos', 'error');
        return;
    }
    
    loading.classList.add('show');
    
    try {
        console.log(`[RegenerateMeal] Regenerating ${mealType} for day: ${currentDay} (index: ${dayIndex})`);
        
        const response = await fetch('/api/menu/regenerate-meal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                week_start_date: currentViewingWeek || getCurrentWeekStart(),
                day_index: dayIndex,
                day_name: currentDay,
                meal_type: mealType,
                current_menu_data: window.currentMenuDataForDays
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`${mealType.charAt(0).toUpperCase() + mealType.slice(1)} regenerado exitosamente`, 'success');
            
            // Update the menu data with the regenerated meal
            if (result.data && result.data.menu_data) {
                window.currentMenuDataForDays = result.data.menu_data;
                
                // Re-render the menu to show the updated meal
                displayMenu(result.data.menu_data);
            }
        } else {
            showAlert('Error al regenerar la comida: ' + (result.error || 'Error desconocido'), 'error');
        }
    } catch (error) {
        console.error('Error regenerating individual meal:', error);
        showAlert('Error al regenerar la comida: ' + (error.message || 'Error de conexión'), 'error');
    } finally {
        loading.classList.remove('show');
    }
}

// Load current week menu (default) - with fallback to latest
async function loadCurrentWeekMenu() {
    const display = document.getElementById('menu-display');
    
    try {
        // Always start with current week - calculate fresh to ensure accuracy
        const currentWeekStart = getCurrentWeekStart();
        console.log('[LoadCurrentWeekMenu] Calculated current week start:', currentWeekStart);
        currentViewingWeek = currentWeekStart;
        
        // Set selectedDayIndex to current day when loading current week menu
        const today = new Date();
        const dayOfWeek = today.getDay();
        const dayMap = [6, 0, 1, 2, 3, 4, 5]; // Sunday=6, Monday=0, etc.
        const currentDayIndex = dayMap[dayOfWeek];
        window.selectedDayIndex = currentDayIndex >= 0 ? currentDayIndex : 0;
        console.log('[LoadCurrentWeekMenu] Setting selectedDayIndex to current day:', window.selectedDayIndex);
        
        // Try to load current week menu - use fetch directly to handle 404 silently
        let result;
        try {
            const response = await fetch('/api/menu/current-week');
            if (response.status === 404) {
                // No menu for current week - show empty state silently
                console.log('[LoadCurrentWeekMenu] No menu for current week:', currentWeekStart);
                
                // Check if menu exists (silently) to update button text
                setTimeout(async () => {
                    const exists = await checkMenuExists(currentViewingWeek);
                    updateWeekNavigation();
                }, 100);
                
                showEmptyWeekState(currentWeekStart);
                updateGenerateButtonForWeek(currentWeekStart);
                return;
            }
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            result = await response.json();
        } catch (error) {
            if (error.message && error.message.includes('404')) {
                // No menu for current week - show empty state silently
                console.log('[LoadCurrentWeekMenu] No menu for current week:', currentWeekStart);
                
                // Check if menu exists (silently) to update button text
                setTimeout(async () => {
                    const exists = await checkMenuExists(currentViewingWeek);
                    updateWeekNavigation();
                }, 100);
                
                showEmptyWeekState(currentWeekStart);
                updateGenerateButtonForWeek(currentWeekStart);
                return;
            }
            throw error; // Re-throw if it's not a 404
        }
        
        if (result.success && result.data) {
            // Use the actual week_start from response, but verify it matches current week
            const weekStart = result.week_start || result.data.week_start_date;
            const calculatedCurrentWeek = getCurrentWeekStart();
            
            if (weekStart) {
                // Verify the week_start matches our calculation for current week
                // If it's different, it might be an old menu, but we'll use it anyway
                if (weekStart === calculatedCurrentWeek) {
                    currentViewingWeek = weekStart;
                    console.log('[LoadCurrentWeekMenu] Set currentViewingWeek to:', currentViewingWeek, '(matches calculated current week)');
                } else {
                    // Backend returned a different week - use it (might be viewing a different week)
                    currentViewingWeek = weekStart;
                    console.log('[LoadCurrentWeekMenu] Set currentViewingWeek to:', currentViewingWeek, '(different from calculated:', calculatedCurrentWeek, ')');
                }
            } else {
                // No week_start in response, use calculated
                currentViewingWeek = calculatedCurrentWeek;
                console.log('[LoadCurrentWeekMenu] No week_start in response, using calculated:', currentViewingWeek);
            }
            updateWeekNavigation();
            
            let menuData = result.data.menu_data;
            
            // Check if menuData is a single meal instead of full menu structure
            if (menuData && menuData.nombre && menuData.ingredientes && !menuData.menu_adultos && !menuData.menu_ninos && !menuData.dias && !menuData.semana) {
                console.warn('[LoadLatestMenu] Menu data appears to be a single meal, checking for full menu structure...');
                
                // Try to use raw_response if available in metadata
                if (result.data.ai_recommendations && result.data.ai_recommendations.raw_response) {
                    try {
                        let rawMenu;
                        const rawResponse = result.data.ai_recommendations.raw_response;
                        
                        if (typeof rawResponse === 'string') {
                            // Try direct parse first
                            try {
                                rawMenu = JSON.parse(rawResponse);
                            } catch (e) {
                                // Try to extract JSON from markdown code block
                                const jsonMatch = rawResponse.match(/```json\s*([\s\S]*?)\s*```/);
                                if (jsonMatch) {
                                    rawMenu = JSON.parse(jsonMatch[1]);
                                } else {
                                    // Try to find JSON object in the string
                                    const jsonObjectMatch = rawResponse.match(/\{[\s\S]*\}/);
                                    if (jsonObjectMatch) {
                                        rawMenu = JSON.parse(jsonObjectMatch[0]);
                                    }
                                }
                            }
                        } else {
                            rawMenu = rawResponse;
                        }
                        
                        if (rawMenu && (rawMenu.menu_adultos || rawMenu.menu_ninos || rawMenu.dias || rawMenu.semana)) {
                            menuData = rawMenu;
                            console.log('[LoadLatestMenu] Using full menu structure from raw_response');
                        }
                    } catch (e) {
                        console.error('[LoadLatestMenu] Failed to parse raw_response:', e);
                    }
                }
            }
            
            displayMenu(menuData);
            
            // Scroll to today's day after a short delay to ensure DOM is ready
            setTimeout(() => {
                scrollToToday();
            }, 500);
        } else {
            // No menu for current week - show empty state
            currentViewingWeek = getCurrentWeekStart();
            updateWeekNavigation();
            showEmptyWeekState(currentViewingWeek);
            updateGenerateButtonForWeek(currentViewingWeek);
        }
    } catch (error) {
        // Handle 404 specifically (no menu available for current week)
        if (error.status === 404) {
            // Try to load latest menu as fallback
            await loadLatestMenuFallback();
        } else {
            console.error('Error loading menu:', error);
            display.innerHTML = `
                <div class="empty-state">
                    <h3>Error al cargar el menú</h3>
                    <p style="margin-top: 1rem; color: var(--silver);">
                        ${error.data?.error || error.message || 'Error desconocido'}
                    </p>
                    <button class="btn btn-primary" onclick="loadCurrentWeekMenu()" style="margin-top: 1.5rem;">
                        Reintentar
                    </button>
                </div>
            `;
            hideWeekNavigation();
        }
    }
}

// Fallback to load latest menu
async function loadLatestMenuFallback() {
    const display = document.getElementById('menu-display');
    
    try {
        const result = await API.get('/api/menu/latest');
        
        if (result.success && result.data) {
            // Extract week_start_date from the menu
            currentViewingWeek = result.data.week_start_date || getCurrentWeekStart();
            updateWeekNavigation();
            
            let menuData = result.data.menu_data;
            
            // Check if menuData is a single meal instead of full menu structure
            if (menuData && menuData.nombre && menuData.ingredientes && !menuData.menu_adultos && !menuData.menu_ninos && !menuData.dias && !menuData.semana) {
                console.warn('[LoadLatestMenu] Menu data appears to be a single meal, checking for full menu structure...');
                
                // Try to use raw_response if available in metadata
                if (result.data.ai_recommendations && result.data.ai_recommendations.raw_response) {
                    try {
                        let rawMenu;
                        const rawResponse = result.data.ai_recommendations.raw_response;
                        
                        if (typeof rawResponse === 'string') {
                            // Try direct parse first
                            try {
                                rawMenu = JSON.parse(rawResponse);
                            } catch (e) {
                                // Try to extract JSON from markdown code block
                                const jsonMatch = rawResponse.match(/```json\s*([\s\S]*?)\s*```/);
                                if (jsonMatch) {
                                    rawMenu = JSON.parse(jsonMatch[1]);
                                } else {
                                    // Try to find JSON object in the string
                                    const jsonObjectMatch = rawResponse.match(/\{[\s\S]*\}/);
                                    if (jsonObjectMatch) {
                                        rawMenu = JSON.parse(jsonObjectMatch[0]);
                                    }
                                }
                            }
                        } else {
                            rawMenu = rawResponse;
                        }
                        
                        if (rawMenu && (rawMenu.menu_adultos || rawMenu.menu_ninos || rawMenu.dias || rawMenu.semana)) {
                            menuData = rawMenu;
                            console.log('[LoadLatestMenu] Using full menu structure from raw_response');
                        }
                    } catch (e) {
                        console.error('[LoadLatestMenu] Failed to parse raw_response:', e);
                    }
                }
            }
            
            displayMenu(menuData);
        } else {
            // No menu available - show empty state
            currentViewingWeek = getCurrentWeekStart();
            updateWeekNavigation();
            showEmptyWeekState(currentViewingWeek);
            updateGenerateButtonForWeek(currentViewingWeek);
        }
    } catch (error) {
        // Handle 404 specifically (no menu available)
        if (error.status === 404) {
            currentViewingWeek = getCurrentWeekStart();
            updateWeekNavigation();
            showEmptyWeekState(currentViewingWeek);
            updateGenerateButtonForWeek(currentViewingWeek);
        } else {
            console.error('Error loading menu:', error);
            display.innerHTML = `
                <div class="empty-state">
                    <h3>Error al cargar el menú</h3>
                    <p style="margin-top: 1rem; color: var(--silver);">
                        ${error.data?.error || error.message || 'Error desconocido'}
                    </p>
                    <button class="btn btn-primary" onclick="loadCurrentWeekMenu()" style="margin-top: 1.5rem;">
                        Reintentar
                    </button>
                </div>
            `;
        }
    }
}

// Update week navigation display
function updateWeekNavigation() {
    const nav = document.getElementById('week-navigation');
    const display = document.getElementById('current-week-display');
    const generateBtn = document.getElementById('generate-menu-btn');
    
    // Always show navigation if we have a week
    if (currentViewingWeek) {
        if (nav) nav.style.display = 'block';
        
        // Format week display nicely
        const weekDate = formatWeekStart(currentViewingWeek);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const weekStart = new Date(currentViewingWeek + 'T00:00:00');
        weekStart.setHours(0, 0, 0, 0);
        
        // Calculate actual current week to compare
        const calculatedCurrentWeek = getCurrentWeekStart();
        const calculatedCurrentWeekDate = new Date(calculatedCurrentWeek + 'T00:00:00');
        
        // Check if this is the actual current calendar week
        const isCurrentWeek = weekStart.getTime() === calculatedCurrentWeekDate.getTime();
        const daysDiff = Math.floor((weekStart - today) / (1000 * 60 * 60 * 24));
        const isNextWeek = daysDiff > 0 && daysDiff <= 7; // Next week
        const isPastWeek = daysDiff < -7; // Past week
        
        if (display) {
            if (isCurrentWeek) {
                display.innerHTML = `<span style="color: var(--gold);">📅 Semana Actual</span><br><span style="font-size: 0.9rem; color: var(--silver);">${weekDate}</span>`;
            } else if (isNextWeek) {
                display.innerHTML = `<span style="color: var(--sage);">📅 Próxima Semana</span><br><span style="font-size: 0.9rem; color: var(--silver);">${weekDate}</span>`;
            } else {
                display.innerHTML = `📅 Semana del ${weekDate}`;
            }
        }
        
        // Update generate button text based on whether menu exists
        if (generateBtn) {
            // Check if menu exists for this week (async, but don't block)
            // Use setTimeout to avoid blocking UI update and reduce console noise
            setTimeout(() => {
                checkMenuExists(currentViewingWeek).then(exists => {
                    if (exists) {
                        generateBtn.textContent = 'Regenerar Menú con IA';
                        generateBtn.title = 'Sobreescribirá el menú existente para esta semana';
                    } else {
                        generateBtn.textContent = 'Generate Menu with AI';
                        generateBtn.title = 'Generar menú para esta semana';
                    }
                }).catch(() => {
                    // Silently ignore errors - default to "Generate"
                    generateBtn.textContent = 'Generate Menu with AI';
                    generateBtn.title = 'Generar menú para esta semana';
                });
            }, 100);
        }
    } else {
        if (nav) nav.style.display = 'none';
        if (generateBtn) {
            generateBtn.textContent = 'Generate Menu with AI';
            generateBtn.title = '';
        }
    }
}

// Check if menu exists for a week (silently handles 404 - no console errors)
async function checkMenuExists(weekStart) {
    try {
        // Use fetch directly to avoid console.error from API.request
        const response = await fetch(`/api/menu/week/${weekStart}`, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            // 404 is expected - no menu exists
            if (response.status === 404) {
                return false;
            }
            // For other errors, return false silently
            return false;
        }
        
        const data = await response.json();
        return data.success && data.data !== null;
    } catch (error) {
        // Silently return false for any error
        return false;
    }
}

// Hide week navigation
function hideWeekNavigation() {
    const nav = document.getElementById('week-navigation');
    if (nav) {
        nav.style.display = 'none';
    }
}

// Scroll to today's day in the menu
function scrollToToday() {
    const todayElement = document.querySelector('[data-day-index]');
    if (todayElement) {
        todayElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Navigate to previous/next week - always navigate, show empty state if no menu
async function navigateWeek(direction) {
    console.log('[NavigateWeek] Navigating', direction, 'from week:', currentViewingWeek);
    
    // If no current week, start from current week
    if (!currentViewingWeek) {
        currentViewingWeek = getCurrentWeekStart();
        console.log('[NavigateWeek] No current week, starting from:', currentViewingWeek);
    }
    
    const currentDate = new Date(currentViewingWeek);
    let targetDate;
    
    if (direction === 'prev') {
        targetDate = new Date(currentDate);
        targetDate.setDate(targetDate.getDate() - 7);
    } else {
        targetDate = new Date(currentDate);
        targetDate.setDate(targetDate.getDate() + 7);
    }
    
    const targetWeekStart = targetDate.toISOString().split('T')[0];
    console.log('[NavigateWeek] Navigating to:', targetWeekStart);
    
    // Always update currentViewingWeek to the target week
    currentViewingWeek = targetWeekStart;
    
    // Check if target week is the current calendar week
    const calculatedCurrentWeek = getCurrentWeekStart();
    const isTargetCurrentWeek = targetWeekStart === calculatedCurrentWeek;
    
    if (isTargetCurrentWeek) {
        // If navigating to current week, set to current day
        const today = new Date();
        const dayOfWeek = today.getDay();
        const dayMap = [6, 0, 1, 2, 3, 4, 5]; // Sunday=6, Monday=0, etc.
        const currentDayIndex = dayMap[dayOfWeek];
        window.selectedDayIndex = currentDayIndex >= 0 ? currentDayIndex : 0;
        console.log('[NavigateWeek] Navigating to current week, setting selectedDayIndex to current day:', window.selectedDayIndex);
    } else {
        // If navigating to other week, set to Monday (0)
        window.selectedDayIndex = 0;
        console.log('[NavigateWeek] Navigating to other week, setting selectedDayIndex to Monday (0)');
    }
    
    updateWeekNavigation();
    
    // Try to load menu for that week - use fetch directly to handle 404 silently
    try {
        let result;
        try {
            const response = await fetch(`/api/menu/week/${targetWeekStart}`);
            if (response.status === 404) {
                // No menu for this week - show empty state silently
                showEmptyWeekState(targetWeekStart);
                return;
            }
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            result = await response.json();
        } catch (error) {
            if (error.message && error.message.includes('404')) {
                // No menu for this week - show empty state silently
                showEmptyWeekState(targetWeekStart);
                updateGenerateButtonForWeek(targetWeekStart);
                return;
            }
            throw error; // Re-throw if it's not a 404
        }
        
        if (result.success && result.data) {
            let menuData = result.data.menu_data;
            
            // Parse menu data if needed
            if (typeof menuData === 'string') {
                try {
                    menuData = JSON.parse(menuData);
                } catch (e) {
                    console.error('Error parsing menu data:', e);
                }
            }
            
            displayMenu(menuData);
            // Update button to show "Regenerar" since menu exists
            updateGenerateButtonForWeek(targetWeekStart);
            setTimeout(() => scrollToToday(), 500);
        } else {
            // No menu for this week - show empty state with generate button
            showEmptyWeekState(targetWeekStart);
            // Update button to show "Generar" since no menu exists
            updateGenerateButtonForWeek(targetWeekStart);
        }
    } catch (error) {
        // Handle other errors (not 404)
        console.error('[NavigateWeek] Error loading menu:', error);
        // Show empty state for any error
        showEmptyWeekState(targetWeekStart);
        // Update button to show "Generar" since no menu exists
        updateGenerateButtonForWeek(targetWeekStart);
    }
}

// Show empty state when navigating to a week without menu
function showEmptyWeekState(weekStart) {
    const display = document.getElementById('menu-display');
    const weekDate = formatWeekStart(weekStart);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const weekStartDate = new Date(weekStart);
    weekStartDate.setHours(0, 0, 0, 0);
    const daysDiff = Math.floor((weekStartDate - today) / (1000 * 60 * 60 * 24));
    const isCurrentWeek = daysDiff >= -7 && daysDiff <= 0;
    const isNextWeek = daysDiff > 0 && daysDiff <= 7;
    
    // Determine week label
    let weekLabel;
    if (isCurrentWeek) {
        weekLabel = '📅 Semana Actual';
    } else if (isNextWeek) {
        weekLabel = '📅 Próxima Semana';
    } else {
        weekLabel = `📅 Semana del ${weekDate}`;
    }
    
    display.innerHTML = `
        <div class="empty-state" style="text-align: center; padding: 3rem;">
            <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1rem; font-size: 2rem;">
                ${weekLabel}
            </h3>
            <p style="color: var(--silver); margin-bottom: 0.5rem; font-size: 1.1rem;">
                ${weekDate}
            </p>
            <p style="color: var(--silver); margin-bottom: 2rem; font-size: 1rem;">
                No hay menú generado para esta semana.
            </p>
            <p style="color: var(--silver); margin-bottom: 2rem;">
                Genera un menú personalizado usando IA para esta semana.
            </p>
            <button class="btn btn-primary" onclick="generateMenu()" style="font-size: 1.1rem; padding: 1.25rem 3rem; margin-bottom: 1rem;">
                🤖 Generar Menú con IA
            </button>
            <p style="color: var(--silver); font-size: 0.85rem; margin-top: 1rem;">
                También puedes usar el botón "Generate Menu with AI" en la parte superior
            </p>
        </div>
    `;
}

// Update generate button text based on whether menu exists for a specific week
async function updateGenerateButtonForWeek(weekStart) {
    const generateBtn = document.getElementById('generate-menu-btn');
    if (!generateBtn) return;
    
    // Check if menu exists for this week
    const exists = await checkMenuExists(weekStart);
    if (exists) {
        generateBtn.textContent = '🔄 Regenerar Menú con IA';
        generateBtn.title = 'Sobreescribirá el menú existente para esta semana';
    } else {
        generateBtn.textContent = '🤖 Generar Menú con IA';
        generateBtn.title = 'Generar menú para esta semana';
    }
}

// Find nearest menu when target week doesn't exist
async function findNearestMenu(targetWeekStart, direction) {
    try {
        console.log('[FindNearestMenu] Looking for nearest menu to:', targetWeekStart, 'direction:', direction);
        
        // Get all menus
        const result = await API.get('/api/menu/all');
        console.log('[FindNearestMenu] All menus result:', result);
        
        if (result.success && result.data && result.data.length > 0) {
            const menus = result.data;
            const targetDate = new Date(targetWeekStart);
            console.log('[FindNearestMenu] Found', menus.length, 'menus');
            
            // Find closest menu in the requested direction
            let closestMenu = null;
            let minDiff = Infinity;
            
            menus.forEach(menu => {
                if (!menu.week_start_date) return;
                
                const menuDate = new Date(menu.week_start_date);
                const diff = Math.abs(menuDate - targetDate);
                
                // Check if menu is in the right direction
                if (direction === 'next' && menuDate >= targetDate) {
                    if (diff < minDiff) {
                        minDiff = diff;
                        closestMenu = menu;
                    }
                } else if (direction === 'prev' && menuDate <= targetDate) {
                    if (diff < minDiff) {
                        minDiff = diff;
                        closestMenu = menu;
                    }
                }
            });
            
            // If no menu in requested direction, find closest overall
            if (!closestMenu && menus.length > 0) {
                menus.forEach(menu => {
                    if (!menu.week_start_date) return;
                    const menuDate = new Date(menu.week_start_date);
                    const diff = Math.abs(menuDate - targetDate);
                    if (diff < minDiff) {
                        minDiff = diff;
                        closestMenu = menu;
                    }
                });
            }
            
            if (closestMenu) {
                const foundWeekStart = closestMenu.week_start_date;
                console.log('[FindNearestMenu] Found closest menu:', foundWeekStart, 'current:', currentViewingWeek);
                
                // Only update if it's different from current
                if (foundWeekStart && foundWeekStart !== currentViewingWeek) {
                    currentViewingWeek = foundWeekStart;
                    updateWeekNavigation();
                    
                    let menuData = closestMenu.menu_data;
                    if (typeof menuData === 'string') {
                        try {
                            menuData = JSON.parse(menuData);
                        } catch (e) {
                            console.error('[FindNearestMenu] Error parsing menu data:', e);
                        }
                    }
                    
                    displayMenu(menuData);
                    setTimeout(() => scrollToToday(), 500);
                    
                    const weekDate = formatWeekStart(foundWeekStart);
                    showAlert(`Mostrando menú disponible más cercano: ${weekDate}`, 'info');
                } else {
                    const weekDate = foundWeekStart ? formatWeekStart(foundWeekStart) : 'esta semana';
                    showAlert(`Ya estás viendo el menú más cercano disponible (${weekDate}). No hay menús ${direction === 'next' ? 'posteriores' : 'anteriores'} a esta fecha.`, 'info');
                }
            } else {
                console.log('[FindNearestMenu] No menu found in direction');
                showAlert(`No hay menús disponibles ${direction === 'prev' ? 'anteriores' : 'posteriores'} a esta fecha. Genera un menú primero.`, 'warning');
            }
        } else {
            console.log('[FindNearestMenu] No menus available');
            showAlert(`No hay menús disponibles. Genera un menú primero usando el botón "Generate Menu with AI".`, 'warning');
        }
    } catch (error) {
        console.error('[FindNearestMenu] Error:', error);
        showAlert(`No se pudo encontrar un menú disponible. Error: ${error.message || 'Desconocido'}`, 'error');
    }
}

function displayMenu(menuData) {
    const display = document.getElementById('menu-display');
    
    // Debug: Log the menu data structure
    console.log('[DisplayMenu] Menu data received:', menuData);
    console.log('[DisplayMenu] Type:', typeof menuData);
    
    if (!menuData) {
        display.innerHTML = `
            <div class="empty-state">
                <h3>Error: No hay datos del menú</h3>
                <p style="margin-top: 1rem; color: var(--silver);">
                    El menú no se generó correctamente. Intenta de nuevo.
                </p>
            </div>
        `;
        return;
    }
    
    // If menuData is a string, try to parse it as JSON
    if (typeof menuData === 'string') {
        try {
            menuData = JSON.parse(menuData);
            console.log('[DisplayMenu] Parsed JSON string:', menuData);
        } catch (e) {
            console.error('[DisplayMenu] Error parsing JSON:', e);
            // If it's not JSON, treat it as plain text
            display.innerHTML = `
                <div class="menu-display">
                    <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1.5rem;">Menú Semanal Generado</h3>
                    <div style="background: rgba(255, 255, 255, 0.03); padding: 2rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
                        <pre style="white-space: pre-wrap; font-family: 'Inter', sans-serif; line-height: 1.8; color: var(--silver); font-size: 0.95rem; margin: 0;">
${menuData}
                        </pre>
                    </div>
                </div>
            `;
            return;
        }
    }
    
    // If it's text format, try to extract JSON from it
    if (menuData.formato === 'texto' || (menuData.contenido && !menuData.menu_adultos && !menuData.menu_ninos)) {
        const contenido = menuData.contenido || '';
        console.log('[DisplayMenu] Text format detected, attempting to extract JSON from contenido');
        
        // Try to find JSON in the contenido (might be in markdown code block)
        const jsonMatch = contenido.match(/```json\s*([\s\S]*?)\s*```/);
        if (jsonMatch) {
            try {
                const jsonStr = jsonMatch[1].trim();
                console.log('[DisplayMenu] Found JSON in markdown block, parsing...');
                const parsedMenu = JSON.parse(jsonStr);
                console.log('[DisplayMenu] Successfully parsed JSON from contenido');
                // Recursively call displayMenu with parsed data
                displayMenu(parsedMenu);
                return;
            } catch (e) {
                console.error('[DisplayMenu] Failed to parse JSON from contenido:', e);
            }
        }
        
        // Try to find any JSON object in the contenido
        const jsonObjectMatch = contenido.match(/\{[\s\S]*\}/);
        if (jsonObjectMatch) {
            try {
                let jsonStr = jsonObjectMatch[0];
                console.log('[DisplayMenu] Found JSON object in contenido, cleaning and parsing...');
                console.log('[DisplayMenu] JSON length:', jsonStr.length);
                
                // Clean up JSON: remove comments (// and /* */)
                jsonStr = jsonStr.replace(/\/\/.*?$/gm, ''); // Remove single-line comments
                jsonStr = jsonStr.replace(/\/\*[\s\S]*?\*\//g, ''); // Remove multi-line comments
                
                // Remove trailing commas before } or ]
                jsonStr = jsonStr.replace(/,(\s*[}\]])/g, '$1');
                
                // Repair unescaped quotes using state machine BEFORE first parse attempt
                function repairJsonString(str) {
                    const result = [];
                    let inString = false;
                    let escapeNext = false;
                    
                    for (let i = 0; i < str.length; i++) {
                        const char = str[i];
                        
                        if (escapeNext) {
                            result.push(char);
                            escapeNext = false;
                        } else if (char === '\\') {
                            result.push(char);
                            escapeNext = true;
                        } else if (char === '"') {
                            if (inString) {
                                // We're inside a string value
                                // Look ahead to determine if this is a closing quote or an unescaped quote
                                let lookahead = i + 1;
                                // Skip whitespace
                                while (lookahead < str.length && /[\s\t\n\r]/.test(str[lookahead])) {
                                    lookahead++;
                                }
                                
                                if (lookahead < str.length) {
                                    const nextChar = str[lookahead];
                                    // If next char is : or , or } or ] or newline, this is likely a closing quote
                                    if (/[:,\n}\]\]]/.test(nextChar)) {
                                        result.push(char);
                                        inString = false;
                                    } else {
                                        // This looks like an unescaped quote inside the string value
                                        // Escape it
                                        result.push('\\"');
                                    }
                                } else {
                                    // End of string, this is a closing quote
                                    result.push(char);
                                    inString = false;
                                }
                            } else {
                                // Starting a new string
                                result.push(char);
                                inString = true;
                            }
                        } else {
                            result.push(char);
                        }
                    }
                    
                    return result.join('');
                }
                
                // Apply repair BEFORE parsing
                jsonStr = repairJsonString(jsonStr);
                console.log('[DisplayMenu] Applied JSON repair before parsing');
                
                // Try to parse
                const parsedMenu = JSON.parse(jsonStr);
                console.log('[DisplayMenu] Successfully parsed JSON object from contenido');
                // Recursively call displayMenu with parsed data
                displayMenu(parsedMenu);
                return;
            } catch (e) {
                console.error('[DisplayMenu] Failed to parse JSON object from contenido:', e);
                console.error('[DisplayMenu] Error message:', e.message);
                
                // Try to show a more helpful error message
                const errorPosMatch = e.message.match(/position (\d+)/);
                if (errorPosMatch) {
                    const pos = parseInt(errorPosMatch[1]);
                    const start = Math.max(0, pos - 200);
                    const end = Math.min(jsonObjectMatch[0].length, pos + 200);
                    const context = jsonObjectMatch[0].substring(start, end);
                    console.error('[DisplayMenu] JSON around error position', pos, ':');
                    console.error(context);
                    
                    // Try a more aggressive fix: repair JSON using state machine
                    try {
                        let fixedJson = jsonObjectMatch[0];
                        
                        // Remove comments
                        fixedJson = fixedJson.replace(/\/\/.*?$/gm, '');
                        fixedJson = fixedJson.replace(/\/\*[\s\S]*?\*\//g, '');
                        
                        // Remove trailing commas
                        fixedJson = fixedJson.replace(/,(\s*[}\]])/g, '$1');
                        
                        // Repair unescaped quotes using state machine
                        function repairJsonString(str) {
                            const result = [];
                            let inString = false;
                            let escapeNext = false;
                            
                            for (let i = 0; i < str.length; i++) {
                                const char = str[i];
                                
                                if (escapeNext) {
                                    result.push(char);
                                    escapeNext = false;
                                } else if (char === '\\') {
                                    result.push(char);
                                    escapeNext = true;
                                } else if (char === '"') {
                                    if (inString) {
                                        // Inside a string, check if this should be escaped
                                        // Look ahead to see what comes after
                                        let lookahead = i + 1;
                                        while (lookahead < str.length && /[\s\t\n\r]/.test(str[lookahead])) {
                                            lookahead++;
                                        }
                                        
                                        if (lookahead < str.length) {
                                            const nextChar = str[lookahead];
                                            // If next char is : or , or } or ], this is likely a closing quote
                                            if (/[:,\n}\]\]]/.test(nextChar)) {
                                                result.push(char);
                                                inString = false;
                                            } else {
                                                // This is an unescaped quote inside the string
                                                result.push('\\"');
                                            }
                                        } else {
                                            result.push(char);
                                            inString = false;
                                        }
                                    } else {
                                        // Starting a new string
                                        result.push(char);
                                        inString = true;
                                    }
                                } else {
                                    result.push(char);
                                }
                            }
                            
                            return result.join('');
                        }
                        
                        fixedJson = repairJsonString(fixedJson);
                        const parsedMenu = JSON.parse(fixedJson);
                        console.log('[DisplayMenu] Successfully parsed JSON after repair');
                        displayMenu(parsedMenu);
                        return;
                    } catch (e2) {
                        console.error('[DisplayMenu] Repair attempt also failed:', e2);
                        if (e2.message && e2.message.match(/position (\d+)/)) {
                            const pos = parseInt(e2.message.match(/position (\d+)/)[1]);
                            const start = Math.max(0, pos - 200);
                            const end = Math.min(jsonObjectMatch[0].length, pos + 200);
                            console.error('[DisplayMenu] JSON around error after repair:', jsonObjectMatch[0].substring(start, end));
                        }
                    }
                }
            }
        }
        
        // If no JSON found, show as text
        display.innerHTML = `
            <div class="menu-display">
                <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1.5rem;">Menú Semanal Generado</h3>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 2rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <pre style="white-space: pre-wrap; font-family: 'Inter', sans-serif; line-height: 1.8; color: var(--silver); font-size: 0.95rem; margin: 0;">
${contenido || 'No hay contenido disponible'}
                    </pre>
                </div>
            </div>
        `;
        return;
    }
    
    // Check if it's a structured menu (has menu_adultos or menu_ninos or dias)
    // Also check if it might be nested in a different structure
    let actualMenuData = menuData;
    
    // Try to find menu data in different possible locations
    if (!menuData.menu_adultos && !menuData.menu_ninos && !menuData.dias) {
        // Check if menu is nested inside another property
        if (menuData.menu && (menuData.menu.menu_adultos || menuData.menu.menu_ninos || menuData.menu.dias)) {
            actualMenuData = menuData.menu;
            console.log('[DisplayMenu] Found menu nested in .menu property');
        } else if (menuData.data && (menuData.data.menu_adultos || menuData.data.menu_ninos || menuData.data.dias)) {
            actualMenuData = menuData.data;
            console.log('[DisplayMenu] Found menu nested in .data property');
        } else if (menuData.menu_data && (menuData.menu_data.menu_adultos || menuData.menu_data.menu_ninos || menuData.menu_data.dias)) {
            actualMenuData = menuData.menu_data;
            console.log('[DisplayMenu] Found menu nested in .menu_data property');
        }
    }
    
    const hasStructuredMenu = actualMenuData.menu_adultos || actualMenuData.menu_ninos || actualMenuData.dias;
    
    console.log('[DisplayMenu] Checking structure - hasStructuredMenu:', hasStructuredMenu);
    console.log('[DisplayMenu] menu_adultos:', !!actualMenuData.menu_adultos);
    console.log('[DisplayMenu] menu_ninos:', !!actualMenuData.menu_ninos);
    console.log('[DisplayMenu] dias:', !!actualMenuData.dias);
    console.log('[DisplayMenu] Available keys:', Object.keys(actualMenuData));
    
    if (!hasStructuredMenu) {
        // Log all keys for debugging
        console.warn('[DisplayMenu] Menu data does not have expected structure.');
        console.warn('[DisplayMenu] Full menu data:', JSON.stringify(actualMenuData, null, 2));
        
        // Try to render anyway if there's any menu-like structure
        // Check if there are any day-like keys at the root level
        const dayKeys = Object.keys(actualMenuData).filter(key => 
            ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'].includes(key.toLowerCase())
        );
        
        if (dayKeys.length > 0) {
            console.log('[DisplayMenu] Found day keys at root, attempting to render:', dayKeys);
            // Try to render with dias structure
            const tempMenuData = { ...actualMenuData };
            tempMenuData.dias = {};
            dayKeys.forEach(day => {
                tempMenuData.dias[day] = actualMenuData[day];
            });
            actualMenuData = tempMenuData;
            // Continue with rendering below
        } else {
            // Check for meal-type structure (desayuno, comida, cena)
            const mealTypeKeys = Object.keys(actualMenuData).filter(key =>
                ['desayuno', 'comida', 'cena', 'almuerzo', 'merienda'].includes(key.toLowerCase())
            );
            
            if (mealTypeKeys.length > 0) {
                console.log('[DisplayMenu] Found meal-type structure, rendering:', mealTypeKeys);
                renderMealTypeMenu(actualMenuData, display);
                return;
            }
            
            // Check if it's a raw_response that needs parsing
            if (actualMenuData.raw_response) {
                console.log('[DisplayMenu] Found raw_response, attempting to parse');
                try {
                    const parsed = JSON.parse(actualMenuData.raw_response);
                    if (parsed.menu_adultos || parsed.menu_ninos || parsed.dias) {
                        actualMenuData = parsed;
                        console.log('[DisplayMenu] Successfully parsed raw_response');
                    }
                } catch (e) {
                    console.error('[DisplayMenu] Failed to parse raw_response:', e);
                }
            }
            
            // Final check - if still no structure, try to extract from raw_response if available
            const finalCheck = actualMenuData.menu_adultos || actualMenuData.menu_ninos || actualMenuData.dias;
            if (!finalCheck) {
                // Check if there's a raw_response that might contain the menu
                if (actualMenuData.raw_response && typeof actualMenuData.raw_response === 'string') {
                    try {
                        const parsedRaw = JSON.parse(actualMenuData.raw_response);
                        if (parsedRaw.menu_adultos || parsedRaw.menu_ninos || parsedRaw.dias) {
                            console.log('[DisplayMenu] Found menu in raw_response, using it');
                            actualMenuData = parsedRaw;
                            // Continue with rendering
                        } else {
                            throw new Error('No menu structure in raw_response');
                        }
                    } catch (e) {
                        console.error('[DisplayMenu] Cannot parse raw_response:', e);
                        // Show helpful message instead of raw JSON
                        display.innerHTML = `
                            <div class="menu-display">
                                <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1.5rem;">Menú Generado</h3>
                                <div style="background: rgba(255, 255, 255, 0.03); padding: 2rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
                                    <p style="color: var(--gold); margin-bottom: 1rem; font-size: 1rem;">
                                        El menú se generó pero tiene una estructura inesperada.
                                    </p>
                                    <p style="color: var(--silver); margin-bottom: 1rem; font-size: 0.95rem;">
                                        Por favor, revisa la consola del navegador (F12) para ver los detalles técnicos.
                                    </p>
                                    <p style="color: var(--silver); font-size: 0.9rem;">
                                        Claves encontradas: ${Object.keys(actualMenuData).slice(0, 10).join(', ')}${Object.keys(actualMenuData).length > 10 ? '...' : ''}
                                    </p>
                                </div>
                            </div>
                        `;
                        return;
                    }
                } else {
                    // Show helpful message instead of raw JSON
                    display.innerHTML = `
                        <div class="menu-display">
                            <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1.5rem;">Menú Generado</h3>
                            <div style="background: rgba(255, 255, 255, 0.03); padding: 2rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
                                <p style="color: var(--gold); margin-bottom: 1rem; font-size: 1rem;">
                                    El menú se generó pero tiene una estructura inesperada.
                                </p>
                                <p style="color: var(--silver); margin-bottom: 1rem; font-size: 0.95rem;">
                                    Por favor, revisa la consola del navegador (F12) para ver los detalles técnicos.
                                </p>
                                <p style="color: var(--silver); font-size: 0.9rem;">
                                    Claves encontradas: ${Object.keys(actualMenuData).slice(0, 10).join(', ')}${Object.keys(actualMenuData).length > 10 ? '...' : ''}
                                </p>
                            </div>
                        </div>
                    `;
                    return;
                }
            }
        }
    }
    
    // Use the actual menu data for rendering
    menuData = actualMenuData;
    
    console.log('[DisplayMenu] Rendering structured menu UI');
    console.log('[DisplayMenu] Using menuData with keys:', Object.keys(menuData));
    console.log('[DisplayMenu] menu_adultos exists:', !!menuData.menu_adultos);
    console.log('[DisplayMenu] menu_ninos exists:', !!menuData.menu_ninos);
    console.log('[DisplayMenu] dias exists:', !!menuData.dias);
    
    // Display structured menu with beautiful UI
    let html = '<div class="menu-display" style="max-width: 100%;">';
    
    // Add rating section at the top
    const currentMenuId = window.currentMenuId || null;
    if (currentMenuId) {
        const currentRating = window.currentMenuRating || null;
        html += `
            <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; background: rgba(255, 255, 255, 0.05); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
                <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1rem; font-size: 1.3rem;">
                    ¿Te gustó este menú?
                </h3>
                <div id="menu-rating" style="display: flex; justify-content: center; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                    ${[1, 2, 3, 4, 5].map(star => `
                        <button 
                            onclick="rateMenu(${currentMenuId}, ${star})"
                            style="
                                background: none;
                                border: none;
                                font-size: 2.5rem;
                                cursor: pointer;
                                padding: 0.25rem;
                                transition: transform 0.2s;
                            "
                            onmouseover="this.style.transform='scale(1.2)'"
                            onmouseout="this.style.transform='scale(1)'"
                            title="${star} ${star === 1 ? 'estrella' : 'estrellas'}"
                        >
                            ${currentRating && currentRating >= star ? '⭐' : '☆'}
                        </button>
                    `).join('')}
                </div>
                ${currentRating ? `
                    <p style="color: var(--gold); margin-top: 0.5rem; font-size: 0.9rem;">
                        Calificado con ${currentRating} ${currentRating === 1 ? 'estrella' : 'estrellas'}
                    </p>
                ` : ''}
            </div>
        `;
    }
    
    // REMOVED: Header section (title, date, recommendations) - user requested removal
    
    const dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
    const diasES = {
        'lunes': 'Lunes',
        'martes': 'Martes',
        'miercoles': 'Miércoles',
        'jueves': 'Jueves',
        'viernes': 'Viernes',
        'sabado': 'Sábado',
        'domingo': 'Domingo'
    };
    
    const diasEN = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miercoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sabado': 'Saturday',
        'domingo': 'Sunday'
    };
    
    const mesesES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
    const mesesEN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    
    // Get week start (Monday) - use currentViewingWeek if available, otherwise current week
    function getWeekStartForDisplay() {
        // Always recalculate current week to ensure accuracy
        const actualCurrentWeek = getCurrentWeekStart();
        
        if (currentViewingWeek) {
            // Use the week being viewed
            const weekStart = new Date(currentViewingWeek + 'T00:00:00');
            weekStart.setHours(0, 0, 0, 0);
            console.log('[getWeekStartForDisplay] Using currentViewingWeek:', currentViewingWeek, '->', weekStart.toISOString().split('T')[0]);
            return weekStart;
        } else {
            // Fallback to current week
            const today = new Date();
            const monday = getMondayOfWeek(today);
            console.log('[getWeekStartForDisplay] No currentViewingWeek, using calculated:', monday.toISOString().split('T')[0]);
            return monday;
        }
    }
    
    // Get date for a specific day of the week (0 = Monday, 6 = Sunday)
    function getDateForDay(dayIndex) {
        const weekStart = getWeekStartForDisplay();
        const date = new Date(weekStart);
        date.setDate(weekStart.getDate() + dayIndex);
        return date;
    }
    
    // Get formatted day with calendar date (e.g., "Miércoles 31" / "Wednesday 31")
    function getDayWithDate(dayKey, lang = 'es') {
        const dayIndex = dias.indexOf(dayKey);
        if (dayIndex === -1) return dayKey;
        
        const date = getDateForDay(dayIndex);
        const dayName = lang === 'es' ? diasES[dayKey] : diasEN[dayKey];
        const dayNumber = date.getDate();
        
        return `${dayName} ${dayNumber}`;
    }
    
    // Get current day of week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
    // Always calculate the actual current week to compare
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const actualCurrentWeekStart = getCurrentWeekStart();
    const actualCurrentWeekStartDate = new Date(actualCurrentWeekStart + 'T00:00:00');
    
    const viewingWeekStart = getWeekStartForDisplay();
    const viewingWeekStartDate = new Date(viewingWeekStart + 'T00:00:00');
    const viewingWeekEnd = new Date(viewingWeekStartDate);
    viewingWeekEnd.setDate(viewingWeekStartDate.getDate() + 6);
    
    // Check if we're viewing the actual current calendar week
    const isViewingCurrentWeek = viewingWeekStartDate.getTime() === actualCurrentWeekStartDate.getTime();
    
    console.log('[DisplayMenu] Today:', today.toISOString().split('T')[0]);
    console.log('[DisplayMenu] Actual current week start:', actualCurrentWeekStart);
    console.log('[DisplayMenu] Viewing week start:', viewingWeekStart);
    console.log('[DisplayMenu] Is viewing current week:', isViewingCurrentWeek);
    
    const dayOfWeek = today.getDay(); // 0-6 (0=Sunday, 1=Monday, etc.)
    // Convert to our format: 0=Monday->lunes, 1=Tuesday->martes, etc.
    // JavaScript: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday
    // Our format: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday
    const dayMap = [6, 0, 1, 2, 3, 4, 5]; // Sunday=6, Monday=0, Tuesday=1, etc.
    const currentDayIndex = isViewingCurrentWeek ? dayMap[dayOfWeek] : -1; // Only use today if viewing current week
    
    // Always use current day when viewing current week, otherwise use stored selectedDayIndex or default to Monday
    let selectedDayIndex;
    if (isViewingCurrentWeek && currentDayIndex >= 0) {
        // Always use current day when viewing current week
        selectedDayIndex = currentDayIndex;
        console.log('[DisplayMenu] Viewing current week, using current day index:', selectedDayIndex);
    } else if (window.selectedDayIndex !== undefined && window.selectedDayIndex >= 0 && window.selectedDayIndex <= 6) {
        // Use stored selectedDayIndex if available and valid (when viewing other weeks)
        selectedDayIndex = window.selectedDayIndex;
        console.log('[DisplayMenu] Using stored selectedDayIndex:', selectedDayIndex);
    } else {
        // Default to Monday
        selectedDayIndex = 0;
        console.log('[DisplayMenu] Defaulting to Monday (index 0)');
    }
    
    console.log('[DisplayMenu] Day of week (JS):', dayOfWeek, '-> Our index:', currentDayIndex);
    console.log('[DisplayMenu] Is viewing current week:', isViewingCurrentWeek);
    console.log('[DisplayMenu] Final selected day index:', selectedDayIndex);
    
    // Store menu data globally for day navigation
    window.currentMenuDataForDays = menuData;
    
    const mealIcons = {
        'desayuno': { emoji: '🌅', color: '#FBBF24', name: 'Desayuno' },
        'comida': { emoji: '🍽️', color: '#10B981', name: 'Comida' },
        'merienda': { emoji: '🧁', color: '#8B5CF6', name: 'Merienda' },
        'cena': { emoji: '🌙', color: '#3B82F6', name: 'Cena' }
    };
    
    // Helper function to render a beautiful meal card
    function renderMealCard(meal, comidaType, dayIndex) {
        const mealInfo = mealIcons[comidaType] || { emoji: '🍽️', color: '#D4AF37', name: comidaType };
        const borderColor = mealInfo.color;
        
        let mealHtml = `
            <div style="background: rgba(255, 255, 255, 0.03); border-left: 4px solid ${borderColor}; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; transition: all 0.3s ease; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                            <span style="font-size: 1.8rem;">${mealInfo.emoji}</span>
                            <h4 style="font-family: 'Playfair Display', serif; font-size: 1.3rem; color: var(--white); margin: 0; font-weight: 700;">
                                ${mealInfo.name}
                            </h4>
                        </div>
                        <h5 style="font-size: 1.4rem; font-weight: 600; color: var(--white); margin-bottom: 1rem; line-height: 1.3;">
                            ${meal.nombre || 'Plato por definir'}
                        </h5>
                    </div>
                    <button 
                        onclick="regenerateIndividualMeal('${comidaType}', ${dayIndex})"
                        style="
                            background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(212, 175, 55, 0.3) 100%);
                            border: 1px solid rgba(212, 175, 55, 0.4);
                            color: var(--gold);
                            padding: 0.5rem 1rem;
                            border-radius: 8px;
                            font-size: 0.8rem;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            white-space: nowrap;
                            font-weight: 500;
                        "
                        onmouseover="this.style.background='linear-gradient(135deg, rgba(212, 175, 55, 0.3) 0%, rgba(212, 175, 55, 0.4) 100%)'; this.style.transform='scale(1.05)'"
                        onmouseout="this.style.background='linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(212, 175, 55, 0.3) 100%)'; this.style.transform='scale(1)'"
                        title="Regenerar esta comida"
                    >
                        🔄 Regenerar
                    </button>
                </div>
        `;
        
        // Recipe base
        if (meal.receta_base) {
            mealHtml += `
                <div style="background: rgba(212, 175, 55, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.75rem; border-left: 3px solid var(--gold);">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.2rem;">📚</span>
                        <div>
                            <div style="font-size: 0.85rem; color: var(--gold); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Basado en receta</div>
                            <div style="font-size: 1rem; color: var(--white); font-weight: 500;">${meal.receta_base}</div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // Related recipes
        if (meal.recetas_relacionadas && meal.recetas_relacionadas.length > 0) {
            mealHtml += `
                <div style="margin-bottom: 0.75rem;">
                    <div style="font-size: 0.85rem; color: var(--silver); margin-bottom: 0.25rem;">🔗 También inspirado en:</div>
                    <div style="font-size: 0.9rem; color: var(--white);">${meal.recetas_relacionadas.join(', ')}</div>
                </div>
            `;
        }
        
        // Why selected
        if (meal.porque_seleccionada) {
            mealHtml += `
                <div style="background: rgba(138, 161, 147, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.75rem;">
                    <div style="font-size: 0.85rem; color: var(--sage); font-style: italic; line-height: 1.6;">
                        ✓ ${meal.porque_seleccionada}
                    </div>
                </div>
            `;
        }
        
        // Details row
        let details = [];
        if (meal.tiempo_prep) details.push(`⏱️ ${meal.tiempo_prep} min`);
        if (meal.ingredientes && meal.ingredientes.length > 0) {
            const ingList = meal.ingredientes.slice(0, 5).join(', ');
            const more = meal.ingredientes.length > 5 ? ` (+${meal.ingredientes.length - 5} más)` : '';
            details.push(`🥘 ${ingList}${more}`);
        }
        
        if (details.length > 0) {
            mealHtml += `
                <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 0.75rem; padding: 0.75rem; background: rgba(255, 255, 255, 0.02); border-radius: 8px;">
                    ${details.map(d => `<span style="font-size: 0.9rem; color: var(--silver);">${d}</span>`).join('')}
                </div>
            `;
        }
        
        // Adaptations
        if (meal.adaptaciones) {
            mealHtml += `
                <div style="background: rgba(212, 175, 55, 0.15); padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; border-left: 3px solid var(--gold);">
                    <div style="font-size: 0.85rem; color: var(--gold); font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">✨ Adaptaciones</div>
                    <div style="font-size: 0.95rem; color: var(--silver); line-height: 1.6;">${meal.adaptaciones}</div>
                </div>
            `;
        }
        
        // Instructions
        if (meal.instrucciones) {
            mealHtml += `
                <div style="margin-bottom: 0.75rem;">
                    <div style="font-size: 0.85rem; color: var(--silver); margin-bottom: 0.5rem;">📖 Preparación:</div>
                    <div style="font-size: 0.95rem; color: var(--white); line-height: 1.6; padding-left: 1rem; border-left: 2px solid rgba(255, 255, 255, 0.1);">
                        ${meal.instrucciones}
                    </div>
                </div>
            `;
        }
        
        // Notes
        if (meal.notas) {
            mealHtml += `
                <div style="background: rgba(138, 161, 147, 0.1); padding: 0.75rem; border-radius: 8px; margin-top: 0.75rem;">
                    <div style="font-size: 0.85rem; color: var(--sage); font-style: italic; line-height: 1.6;">
                        💡 ${meal.notas}
                    </div>
                </div>
            `;
        }
        
        mealHtml += `</div>`;
        return mealHtml;
    }
    
    // Helper function to render a day's meals
    function renderDayMeals(diaData, comidas, dayIndex) {
        let dayHtml = '';
        comidas.forEach(comida => {
            if (diaData[comida]) {
                dayHtml += renderMealCard(diaData[comida], comida, dayIndex);
            }
        });
        return dayHtml;
    }
    
    // Function to render a specific day (must be accessible globally)
    window.renderDayContent = function(dayIndex) {
        const menuDataForDay = window.currentMenuDataForDays || menuData;
        const dia = dias[dayIndex];
        let dayHtml = '';
        
        // MENÚ PARA ADULTOS
        if (menuDataForDay.menu_adultos && menuDataForDay.menu_adultos.dias && menuDataForDay.menu_adultos.dias[dia]) {
            const diaData = menuDataForDay.menu_adultos.dias[dia];
            dayHtml += `
                <div style="margin-bottom: 3rem;">
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <h2 style="font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 600; color: var(--gold); margin-bottom: 0.5rem;">
                            👨‍👩‍👧‍👦 Menú para ADULTOS
                        </h2>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 2rem; border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
                        <div style="background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dark) 100%); color: var(--black); padding: 0.75rem 1.25rem; border-radius: 12px 12px 0 0; margin: -2rem -2rem 1.5rem -2rem; font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 600; text-transform: capitalize;">
                            ${getDayWithDate(dia, 'es')}
                        </div>
                        ${renderDayMeals(diaData, ['desayuno', 'comida', 'cena'], dayIndex)}
                    </div>
                </div>
            `;
        }
        
        // MENÚ PARA NIÑOS
        if (menuDataForDay.menu_ninos && menuDataForDay.menu_ninos.dias && menuDataForDay.menu_ninos.dias[dia]) {
            const diaData = menuDataForDay.menu_ninos.dias[dia];
            dayHtml += `
                <div style="margin-bottom: 3rem;">
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <h2 style="font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 600; color: var(--sage); margin-bottom: 0.5rem;">
                            👶 Menú para NIÑOS
                        </h2>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 2rem; border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
                        <div style="background: linear-gradient(135deg, var(--sage) 0%, #7A9184 100%); color: var(--white); padding: 0.75rem 1.25rem; border-radius: 12px 12px 0 0; margin: -2rem -2rem 1.5rem -2rem; font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 600; text-transform: capitalize;">
                            ${getDayWithDate(dia, 'es')}
                        </div>
                        ${renderDayMeals(diaData, ['desayuno', 'comida', 'merienda', 'cena'], dayIndex)}
                    </div>
                </div>
            `;
        }
        
        return dayHtml;
    };
    
    // Function to switch day
    window.switchDay = function(dayIndex) {
        window.selectedDayIndex = dayIndex;
        const dayContent = document.getElementById('day-content');
        if (dayContent && window.renderDayContent) {
            dayContent.innerHTML = window.renderDayContent(dayIndex);
            
            // Update button styles
            document.querySelectorAll('.day-button').forEach((btn, idx) => {
                if (idx === dayIndex) {
                    btn.style.background = 'linear-gradient(135deg, var(--gold) 0%, var(--gold-dark) 100%)';
                    btn.style.color = 'var(--black)';
                    btn.style.transform = 'scale(1.05)';
                    btn.style.borderColor = 'var(--gold)';
                } else {
                    btn.style.background = 'rgba(255, 255, 255, 0.05)';
                    btn.style.color = 'var(--silver)';
                    btn.style.transform = 'scale(1)';
                    btn.style.borderColor = 'rgba(255, 255, 255, 0.2)';
                }
            });
        }
    };
    
    // Store selectedDayIndex globally - ensure it's valid (0-6)
    window.selectedDayIndex = selectedDayIndex >= 0 ? selectedDayIndex : 0;
    
    // MENÚ PARA ADULTOS - Add day navigation buttons
    if (menuData.menu_adultos && menuData.menu_adultos.dias) {
        html += `
            <div style="margin-bottom: 4rem;">
                <div style="text-align: center; margin-bottom: 1.5rem;">
                    <h2 style="font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; color: var(--gold); margin-bottom: 0.5rem;">
                        📅 Menú Semanal
                    </h2>
                </div>
                
                <!-- Day Navigation Buttons -->
                <div style="display: flex; justify-content: center; gap: 0.75rem; margin-bottom: 2.5rem; flex-wrap: wrap;">
                    ${dias.map((dia, idx) => `
                        <button 
                            class="day-button"
                            onclick="switchDay(${idx})"
                            style="
                                padding: 0.75rem 1.5rem;
                                border-radius: 12px;
                                border: 2px solid ${idx === selectedDayIndex ? 'var(--gold)' : 'rgba(255, 255, 255, 0.2)'};
                                background: ${idx === selectedDayIndex ? 'linear-gradient(135deg, var(--gold) 0%, var(--gold-dark) 100%)' : 'rgba(255, 255, 255, 0.05)'};
                                color: ${idx === selectedDayIndex ? 'var(--black)' : 'var(--silver)'};
                                font-family: 'Playfair Display', serif;
                                font-size: 1rem;
                                font-weight: ${idx === selectedDayIndex ? '700' : '500'};
                                cursor: pointer;
                                transition: all 0.3s ease;
                                text-transform: capitalize;
                                ${idx === selectedDayIndex ? 'transform: scale(1.05);' : ''}
                            "
                            onmouseover="this.style.background='rgba(212, 175, 55, 0.2)'; this.style.borderColor='var(--gold)';"
                            onmouseout="
                                if (${idx} !== window.selectedDayIndex) {
                                    this.style.background='rgba(255, 255, 255, 0.05)';
                                    this.style.borderColor='rgba(255, 255, 255, 0.2)';
                                }
                            "
                        >
                            ${getDayWithDate(dia, 'es')}
                            ${idx === currentDayIndex && currentDayIndex >= 0 ? ' <span style="font-size: 0.8rem;">(Hoy)</span>' : ''}
                        </button>
                    `).join('')}
                </div>
                
                <!-- Day Content Container -->
                <div id="day-content">
                    ${window.renderDayContent(selectedDayIndex)}
                </div>
        `;
        
        html += '</div>';
    } else if (menuData.menu_ninos && menuData.menu_ninos.dias) {
        // If only children menu exists, show it with day navigation
        html += `
            <div style="margin-bottom: 4rem;">
                <div style="text-align: center; margin-bottom: 2.5rem;">
                    <h2 style="font-family: 'Playfair Display', serif; font-size: 2.5rem; font-weight: 900; color: var(--sage); margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: -1px;">
                        📅 Menú Semanal
                    </h2>
                    <div style="width: 100px; height: 3px; background: linear-gradient(90deg, transparent, var(--sage), transparent); margin: 0 auto;"></div>
                </div>
                
                <!-- Day Navigation Buttons -->
                <div style="display: flex; justify-content: center; gap: 0.75rem; margin-bottom: 2.5rem; flex-wrap: wrap;">
                    ${dias.map((dia, idx) => `
                        <button 
                            class="day-button"
                            onclick="switchDay(${idx})"
                            style="
                                padding: 0.75rem 1.5rem;
                                border-radius: 12px;
                                border: 2px solid ${idx === selectedDayIndex ? 'var(--sage)' : 'rgba(255, 255, 255, 0.2)'};
                                background: ${idx === selectedDayIndex ? 'linear-gradient(135deg, var(--sage) 0%, #7A9184 100%)' : 'rgba(255, 255, 255, 0.05)'};
                                color: ${idx === selectedDayIndex ? 'var(--white)' : 'var(--silver)'};
                                font-family: 'Playfair Display', serif;
                                font-size: 1rem;
                                font-weight: ${idx === selectedDayIndex ? '700' : '500'};
                                cursor: pointer;
                                transition: all 0.3s ease;
                                text-transform: capitalize;
                                ${idx === selectedDayIndex ? 'transform: scale(1.05);' : ''}
                            "
                            onmouseover="this.style.background='rgba(138, 161, 147, 0.2)'; this.style.borderColor='var(--sage)';"
                            onmouseout="
                                if (${idx} !== window.selectedDayIndex) {
                                    this.style.background='rgba(255, 255, 255, 0.05)';
                                    this.style.borderColor='rgba(255, 255, 255, 0.2)';
                                }
                            "
                        >
                            ${getDayWithDate(dia, 'es')}
                            ${idx === currentDayIndex && currentDayIndex >= 0 ? ' <span style="font-size: 0.8rem;">(Hoy)</span>' : ''}
                        </button>
                    `).join('')}
                </div>
                
                <!-- Day Content Container -->
                <div id="day-content">
                    ${window.renderDayContent(selectedDayIndex)}
                </div>
        `;
        
        html += '</div>';
    }
    
    // Fallback: Si no hay estructura nueva, mostrar estructura antigua
    if (!menuData.menu_adultos && !menuData.menu_ninos && menuData.dias) {
        html += '<div style="background: #fef3c7; padding: 16px; border-radius: 8px; margin-bottom: 24px; border-left: 4px solid var(--warning);">';
        html += '<strong>⚠️ Menú en formato antiguo</strong><br>';
        html += 'Este menú fue generado antes de la actualización. Genera uno nuevo para ver los menús separados.';
        html += '</div>';
        
        dias.forEach(dia => {
            const diaData = menuData.dias[dia];
            if (!diaData) return;
            
            html += `<div class="day-menu">
                <div class="day-header">${diasES[dia]}</div>`;
            
            ['desayuno', 'comida', 'merienda', 'cena'].forEach(comida => {
                if (diaData[comida]) {
                    const meal = diaData[comida];
                    html += `<div class="meal-item">
                        <div class="meal-title">🍽️ ${comida.charAt(0).toUpperCase() + comida.slice(1)}: ${meal.nombre || 'N/A'}</div>
                        <div class="meal-details">
                            ${meal.tiempo_prep ? `⏱️ ${meal.tiempo_prep} min` : ''}
                        </div>
                        ${meal.notas ? `<div style="font-size: 0.85rem; color: var(--text-light); margin-top: 4px;">💡 ${meal.notas}</div>` : ''}
                    </div>`;
                }
            });
            
            html += '</div>';
        });
    }
    
    // REMOVED: Lista de compra sections - moved to separate Shopping List tab
    
    if (menuData.consejos_preparacion) {
        html += `
            <div style="background: rgba(138, 161, 147, 0.15); padding: 2rem; border-radius: 16px; margin-top: 2rem; border-left: 4px solid var(--sage); backdrop-filter: blur(10px);">
                <div style="display: flex; align-items: flex-start; gap: 1rem;">
                    <span style="font-size: 2rem;">💡</span>
                    <div>
                        <h4 style="font-family: 'Playfair Display', serif; font-size: 1.5rem; color: var(--sage); margin-bottom: 0.75rem;">Consejos de Preparación</h4>
                        <p style="color: var(--silver); line-height: 1.8; font-size: 1rem;">${menuData.consejos_preparacion}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    html += '</div>';
    console.log('[DisplayMenu] HTML generated, length:', html.length, 'characters');
    display.innerHTML = html;
    console.log('[DisplayMenu] Menu displayed successfully');
    
    // Scroll to top of menu display
    if (display) {
        display.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function renderMealTypeMenu(menuData, displayElement) {
    /**
     * Render menu organized by meal types (desayuno, comida, cena)
     * instead of by days of the week
     */
    console.log('[RenderMealTypeMenu] Rendering meal-type menu structure');
    
    const mealTypes = {
        'desayuno': 'Desayuno',
        'comida': 'Comida',
        'almuerzo': 'Almuerzo',
        'cena': 'Cena',
        'merienda': 'Merienda'
    };
    
    let html = '<div class="menu-display" style="max-width: 100%;">';
    
    // Header
    html += `
        <div style="text-align: center; margin-bottom: 2.5rem;">
            <h2 style="font-family: 'Playfair Display', serif; color: var(--gold); font-size: 2.5rem; margin-bottom: 0.5rem; font-weight: 600;">
                Menú Semanal Generado
            </h2>
            <p style="color: var(--silver); font-size: 1rem; font-style: italic;">
                Organizado por tipo de comida
            </p>
        </div>
    `;
    
    // Render each meal type
    Object.keys(menuData).forEach(mealKey => {
        const mealType = mealTypes[mealKey.toLowerCase()] || mealKey;
        const meal = menuData[mealKey];
        
        if (!meal || typeof meal !== 'object') return;
        
        html += `
            <div style="background: rgba(255, 255, 255, 0.03); border-radius: 16px; padding: 2rem; margin-bottom: 2rem; border: 1px solid rgba(255, 255, 255, 0.1);">
                <h3 style="font-family: 'Playfair Display', serif; color: var(--gold); font-size: 1.8rem; margin-bottom: 1.5rem; border-bottom: 2px solid var(--gold); padding-bottom: 0.5rem;">
                    ${mealType.charAt(0).toUpperCase() + mealType.slice(1)}
                </h3>
        `;
        
        // Meal name
        if (meal.nombre) {
            html += `
                <h4 style="font-family: 'Playfair Display', serif; color: var(--white); font-size: 1.4rem; margin-bottom: 1rem;">
                    ${meal.nombre}
                </h4>
            `;
        }
        
        // Ingredients
        if (meal.ingredientes && Array.isArray(meal.ingredientes) && meal.ingredientes.length > 0) {
            html += `
                <div style="margin-bottom: 1rem;">
                    <h5 style="color: var(--gold); font-size: 1rem; margin-bottom: 0.5rem; font-weight: 600;">Ingredientes:</h5>
                    <ul style="color: var(--silver); font-size: 0.95rem; line-height: 1.8; margin-left: 1.5rem;">
                        ${meal.ingredientes.map(ing => `<li>${ing}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        // Instructions
        if (meal.instrucciones) {
            html += `
                <div style="margin-bottom: 1rem;">
                    <h5 style="color: var(--gold); font-size: 1rem; margin-bottom: 0.5rem; font-weight: 600;">Instrucciones:</h5>
                    <p style="color: var(--silver); font-size: 0.95rem; line-height: 1.8;">
                        ${meal.instrucciones}
                    </p>
                </div>
            `;
        }
        
        // Adaptations
        if (meal.adaptaciones) {
            html += `
                <div style="margin-bottom: 1rem; background: rgba(255, 215, 0, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid var(--gold);">
                    <h5 style="color: var(--gold); font-size: 1rem; margin-bottom: 0.5rem; font-weight: 600;">Adaptaciones:</h5>
                    <p style="color: var(--silver); font-size: 0.95rem; line-height: 1.8;">
                        ${meal.adaptaciones}
                    </p>
                </div>
            `;
        }
        
        // Notes
        if (meal.notas) {
            html += `
                <div style="margin-bottom: 1rem;">
                    <h5 style="color: var(--gold); font-size: 1rem; margin-bottom: 0.5rem; font-weight: 600;">Notas:</h5>
                    <p style="color: var(--silver); font-size: 0.95rem; line-height: 1.8; font-style: italic;">
                        ${meal.notas}
                    </p>
                </div>
            `;
        }
        
        // Why selected
        if (meal.porque_seleccionada) {
            html += `
                <div style="margin-bottom: 1rem; background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 8px;">
                    <h5 style="color: var(--gold); font-size: 1rem; margin-bottom: 0.5rem; font-weight: 600;">¿Por qué fue seleccionada?</h5>
                    <p style="color: var(--silver); font-size: 0.95rem; line-height: 1.8;">
                        ${meal.porque_seleccionada}
                    </p>
                </div>
            `;
        }
        
        // Base recipe
        if (meal.receta_base) {
            html += `
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                    <p style="color: var(--silver); font-size: 0.85rem; font-style: italic;">
                        <strong>Receta base:</strong> ${meal.receta_base}
                    </p>
                </div>
            `;
        }
        
        // Preparation time
        if (meal.tiempo_prep) {
            html += `
                <div style="margin-top: 1rem;">
                    <span style="color: var(--gold); font-size: 0.9rem;">
                        ⏱️ Tiempo de preparación: ${meal.tiempo_prep} minutos
                    </span>
                </div>
            `;
        }
        
        html += `</div>`;
    });
    
    html += '</div>';
    
    displayElement.innerHTML = html;
    console.log('[RenderMealTypeMenu] Meal-type menu rendered successfully');
    
    // Scroll to top
    if (displayElement) {
        displayElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Settings functions
async function loadSettings() {
    try {
        const result = await API.get('/api/settings');
        if (result.success) {
            const data = result.data;
            const apiKeyInput = document.getElementById('anthropic-api-key');
            const statusDiv = document.getElementById('api-key-status');
            const modeElement = document.getElementById('system-mode');
            
            // Update system mode
            if (modeElement) {
                modeElement.textContent = data.mode === 'production' ? 'Producción' : 'Desarrollo';
            }
            
            // Show API key status
            if (data.has_api_key) {
                statusDiv.innerHTML = `
                    <div style="padding: 12px; background: rgba(34, 197, 94, 0.1); border-radius: 6px; color: #86EFAC; border: 1px solid rgba(34, 197, 94, 0.3);">
                        ✅ API Key configurada correctamente
                        ${data.api_key_preview ? `<br><small style="font-family: monospace; font-weight: 600; font-size: 0.95rem;">${data.api_key_preview}</small>` : ''}
                        <br><small style="color: #86EFAC; margin-top: 8px; display: block;">
                            💾 La key está guardada en el archivo .env del proyecto
                        </small>
                        <br><button onclick="showFullApiKey()" style="margin-top: 10px; padding: 6px 12px; background: rgba(34, 197, 94, 0.2); border: 1px solid rgba(34, 197, 94, 0.5); color: #86EFAC; border-radius: 4px; cursor: pointer; font-size: 0.9rem;">
                            🔍 Mostrar Key Completa (solo localhost)
                        </button>
                        <div id="full-api-key-display" style="display: none; margin-top: 10px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 4px; font-family: monospace; word-break: break-all;"></div>
                    </div>
                `;
                // Don't fill the input for security, but show placeholder
                if (apiKeyInput) {
                    apiKeyInput.placeholder = data.api_key_preview || 'sk-ant-api03-... (ya configurada)';
                    apiKeyInput.value = '';
                }
            } else {
                statusDiv.innerHTML = `
                    <div style="padding: 12px; background: rgba(251, 191, 36, 0.1); border-radius: 6px; color: #FCD34D; border: 1px solid rgba(251, 191, 36, 0.3);">
                        ⚠️ No hay API Key configurada. Configúrala para generar menús con IA.
                    </div>
                `;
                if (apiKeyInput) {
                    apiKeyInput.placeholder = 'sk-ant-api03-...';
                    apiKeyInput.value = '';
                }
            }
            
            // Load menu preferences
            if (data.menu_preferences) {
                loadMenuPreferences(data.menu_preferences);
            }
        }
    } catch (error) {
        console.error('Error loading settings:', error);
        showAlert('Error al cargar la configuración', 'error');
    }
}

async function showFullApiKey() {
    try {
        const response = await fetch('/api/temp/get-api-key');
        const data = await response.json();
        
        if (data.success && data.api_key) {
            const displayDiv = document.getElementById('full-api-key-display');
            if (displayDiv) {
                displayDiv.innerHTML = `
                    <div style="margin-bottom: 10px;">
                        <strong style="color: #86EFAC;">API Key Completa:</strong>
                        <button onclick="copyFullApiKey()" style="margin-left: 10px; padding: 4px 8px; background: rgba(34, 197, 94, 0.3); border: 1px solid rgba(34, 197, 94, 0.5); color: #86EFAC; border-radius: 4px; cursor: pointer; font-size: 0.85rem;">
                            📋 Copiar
                        </button>
                        <button onclick="saveFullApiKeyToEnv()" style="margin-left: 5px; padding: 4px 8px; background: rgba(34, 197, 94, 0.3); border: 1px solid rgba(34, 197, 94, 0.5); color: #86EFAC; border-radius: 4px; cursor: pointer; font-size: 0.85rem;">
                            💾 Guardar en .env
                        </button>
                    </div>
                    <div id="full-api-key-text" style="color: #CBD5E0; font-size: 0.9rem;">${data.api_key}</div>
                `;
                displayDiv.style.display = 'block';
            }
        } else {
            showAlert('No se pudo obtener la API key: ' + (data.error || 'Error desconocido'), 'error');
        }
    } catch (error) {
        showAlert('Error al obtener la API key: ' + error.message, 'error');
    }
}

function copyFullApiKey() {
    const keyText = document.getElementById('full-api-key-text');
    if (keyText) {
        navigator.clipboard.writeText(keyText.textContent).then(() => {
            showAlert('API Key copiada al portapapeles', 'success');
        }).catch(() => {
            // Fallback: select text
            const range = document.createRange();
            range.selectNode(keyText);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            document.execCommand('copy');
            showAlert('API Key seleccionada - copia manualmente (Ctrl+C)', 'info');
        });
    }
}

async function saveFullApiKeyToEnv() {
    try {
        const response = await fetch('/api/temp/save-api-key-to-env', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            showAlert('✅ ' + data.message, 'success');
        } else {
            showAlert('Error: ' + (data.error || 'Error desconocido'), 'error');
        }
    } catch (error) {
        showAlert('Error al guardar: ' + error.message, 'error');
    }
}

async function loadMenuPreferences(prefs = null) {
    try {
        if (!prefs) {
            const result = await API.get('/api/settings');
            if (result.success && result.data.menu_preferences) {
                prefs = result.data.menu_preferences;
            } else {
                // Use defaults
                prefs = {
                    include_weekend: true,
                    include_breakfast: true,
                    include_lunch: true,
                    include_dinner: true,
                    excluded_days: []
                };
            }
        }
        
        // Update checkboxes
        const includeWeekend = document.getElementById('include-weekend');
        const includeBreakfast = document.getElementById('include-breakfast');
        const includeLunch = document.getElementById('include-lunch');
        const includeDinner = document.getElementById('include-dinner');
        
        if (includeWeekend) includeWeekend.checked = prefs.include_weekend !== false;
        if (includeBreakfast) includeBreakfast.checked = prefs.include_breakfast !== false;
        if (includeLunch) includeLunch.checked = prefs.include_lunch !== false;
        if (includeDinner) includeDinner.checked = prefs.include_dinner !== false;
        
        // Update excluded days
        const excludedDays = prefs.excluded_days || [];
        document.querySelectorAll('.excluded-day').forEach(checkbox => {
            checkbox.checked = excludedDays.includes(checkbox.value);
        });
        
    } catch (error) {
        console.error('Error loading menu preferences:', error);
    }
}

// Settings form submission
const settingsForm = document.getElementById('settingsForm');
if (settingsForm) {
    settingsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const apiKey = formData.get('anthropic_api_key')?.trim();
        
        const dataToSend = {};
        
        // Only include API key if provided
        if (apiKey) {
            if (!apiKey.startsWith('sk-ant-')) {
                showAlert('La API key de Anthropic debe comenzar con "sk-ant-"', 'error');
                return;
            }
            dataToSend.anthropic_api_key = apiKey;
        }
        
        try {
            const result = await API.post('/api/settings', dataToSend);
            
            if (result.success) {
                showAlert('✅ Configuración guardada correctamente.' + (apiKey ? ' Puede que necesites reiniciar el servidor para aplicar los cambios de API key completamente.' : ''), 'success');
                // Clear the input for security
                if (apiKey) {
                    document.getElementById('anthropic-api-key').value = '';
                }
                // Reload settings to show updated status
                setTimeout(() => loadSettings(), 1000);
            }
        } catch (error) {
            showAlert('Error al guardar la configuración: ' + (error.message || 'Error desconocido'), 'error');
        }
    });
}

// Menu preferences form submission
const menuPreferencesForm = document.getElementById('menuPreferencesForm');
if (menuPreferencesForm) {
    menuPreferencesForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const includeWeekend = document.getElementById('include-weekend').checked;
        const includeBreakfast = document.getElementById('include-breakfast').checked;
        const includeLunch = document.getElementById('include-lunch').checked;
        const includeDinner = document.getElementById('include-dinner').checked;
        
        // Validate at least one meal is selected
        if (!includeBreakfast && !includeLunch && !includeDinner) {
            showAlert('Debes seleccionar al menos una comida (Desayuno, Comida o Cena)', 'error');
            return;
        }
        
        // Get excluded days
        const excludedDays = [];
        document.querySelectorAll('.excluded-day:checked').forEach(checkbox => {
            excludedDays.push(checkbox.value);
        });
        
        const menuPreferences = {
            include_weekend: includeWeekend,
            include_breakfast: includeBreakfast,
            include_lunch: includeLunch,
            include_dinner: includeDinner,
            excluded_days: excludedDays
        };
        
        try {
            const result = await API.post('/api/settings', {
                menu_preferences: menuPreferences
            });
            
            if (result.success) {
                showAlert('✅ Preferencias del menú guardadas correctamente', 'success');
                // Reload to show updated preferences
                setTimeout(() => loadMenuPreferences(), 500);
            }
        } catch (error) {
            showAlert('Error al guardar las preferencias: ' + (error.message || 'Error desconocido'), 'error');
        }
    });
}

async function testApiKey() {
    const apiKeyInput = document.getElementById('anthropic-api-key');
    const apiKey = apiKeyInput ? apiKeyInput.value.trim() : '';
    
    if (!apiKey) {
        showAlert('Por favor, introduce una API key para probar', 'error');
        return;
    }
    
    if (!apiKey.startsWith('sk-ant-')) {
        showAlert('La API key de Anthropic debe comenzar con "sk-ant-"', 'error');
        return;
    }
    
    try {
        showAlert('Probando API key...', 'info');
        const result = await API.post('/api/settings/test', {
            anthropic_api_key: apiKey
        });
        
        if (result.success) {
            showAlert('✅ ' + result.message, 'success');
        }
    } catch (error) {
        showAlert('❌ Error al probar la API key: ' + (error.message || 'La key puede ser inválida'), 'error');
    }
}

// TV URL functions
function copyTvUrl() {
    const url = document.getElementById('tv-url').textContent;
    navigator.clipboard.writeText(url).then(() => {
        showAlert('URL copiada al portapapeles', 'success');
    });
}

// Shopping List Global Variables
let shoppingCheckedItems = new Set();
let shoppingTotalItems = 0;
let currentShoppingMenuData = null;
let currentShoppingWeek = null; // Track which week is being viewed in shopping list

// Category mappings
const shoppingCategoryIcons = {
    'frutas_verduras': '🥬',
    'carnes_pescados': '🍖',
    'lacteos_huevos': '🥛',
    'cereales_legumbres': '🌾',
    'despensa': '🏺',
    'congelados': '❄️',
    'otros': '📦'
};

const shoppingCategoryNames = {
    'frutas_verduras': 'Frutas y Verduras',
    'carnes_pescados': 'Carnes y Pescados',
    'lacteos_huevos': 'Lácteos y Huevos',
    'cereales_legumbres': 'Cereales y Legumbres',
    'despensa': 'Despensa',
    'congelados': 'Congelados',
    'otros': 'Otros'
};

// Load shopping list for a specific week
async function loadShoppingLists(weekStartDate = null) {
    const display = document.getElementById('shopping-list-display');
    if (!display) return;
    
    // If no week specified, use current week
    if (!weekStartDate) {
        weekStartDate = getCurrentWeekStart();
    }
    
    // Ensure weekStartDate is normalized to Monday of that week
    // This handles cases where a non-Monday date might be passed
    const dateObj = new Date(weekStartDate + 'T00:00:00');
    const monday = getMondayOfWeek(dateObj);
    const mondayYear = monday.getFullYear();
    const mondayMonth = monday.getMonth();
    const mondayDate = monday.getDate();
    weekStartDate = `${mondayYear}-${String(mondayMonth + 1).padStart(2, '0')}-${String(mondayDate).padStart(2, '0')}`;
    
    // Update current shopping week
    currentShoppingWeek = weekStartDate;
    updateShoppingWeekNavigation();
    
    display.innerHTML = '<div style="text-align: center; padding: 2rem;"><div class="spinner"></div><p style="margin-top: 1rem; color: var(--silver);">Cargando lista de compra...</p></div>';
    
    try {
        console.log('[ShoppingList] Loading shopping list for week:', weekStartDate);
        
        // Load menu for the specified week - use fetch directly to handle 404 silently
        let weekResult;
        try {
            const response = await fetch(`/api/menu/week/${weekStartDate}`);
            if (response.status === 404) {
                // No menu for this week - show empty state
                display.innerHTML = `
                    <div class="empty-state" style="text-align: center; padding: 3rem;">
                        <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1rem; font-size: 2rem;">
                            No hay menú para esta semana
                        </h3>
                        <p style="color: var(--silver); margin-bottom: 2rem;">
                            No hay lista de compra disponible para la semana del ${formatWeekStart(weekStartDate)}
                        </p>
                        <button class="btn btn-primary" onclick="loadShoppingLists(getCurrentWeekStart())" style="margin-top: 1rem;">
                            📅 Ver Semana Actual
                        </button>
                    </div>
                `;
                return;
            }
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            weekResult = await response.json();
        } catch (error) {
            if (error.message && error.message.includes('404')) {
                // No menu for this week - show empty state
                display.innerHTML = `
                    <div class="empty-state" style="text-align: center; padding: 3rem;">
                        <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1rem; font-size: 2rem;">
                            No hay menú para esta semana
                        </h3>
                        <p style="color: var(--silver); margin-bottom: 2rem;">
                            No hay lista de compra disponible para la semana del ${formatWeekStart(weekStartDate)}
                        </p>
                        <button class="btn btn-primary" onclick="loadShoppingLists(getCurrentWeekStart())" style="margin-top: 1rem;">
                            📅 Ver Semana Actual
                        </button>
                    </div>
                `;
                return;
            }
            throw error; // Re-throw if it's not a 404
        }
        
        let weekMenu = null;
        let weekMenuData = null;
        
        // Process week result
        if (weekResult.success && weekResult.data) {
            weekMenu = weekResult.data;
            console.log('[ShoppingList] Week menu loaded:', weekMenu);
            
            if (weekMenu && weekMenu.menu_data) {
                try {
                    weekMenuData = typeof weekMenu.menu_data === 'string' 
                        ? JSON.parse(weekMenu.menu_data) 
                        : weekMenu.menu_data;
                    console.log('[ShoppingList] Week menu data parsed successfully');
                } catch (e) {
                    console.error('[ShoppingList] Failed to parse week menu data:', e);
                    weekMenuData = null;
                }
            }
        } else {
            // No menu for this week
            display.innerHTML = `
                <div class="empty-state" style="text-align: center; padding: 3rem;">
                    <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1rem; font-size: 2rem;">
                        No hay menú para esta semana
                    </h3>
                    <p style="color: var(--silver); margin-bottom: 2rem;">
                        No hay lista de compra disponible para la semana del ${formatWeekStart(weekStartDate)}
                    </p>
                    <button class="btn btn-primary" onclick="loadShoppingLists(getCurrentWeekStart())" style="margin-top: 1rem;">
                        📅 Ver Semana Actual
                    </button>
                </div>
            `;
            return;
        }
        
        // Load family composition
        await loadFamilyComposition();
        
        // Build HTML - use same logic as updateShoppingWeekNavigation
        const weekStartFormatted = formatWeekStart(weekStartDate);
        const weekStartDateObj = new Date(weekStartDate + 'T00:00:00');
        weekStartDateObj.setHours(0, 0, 0, 0);
        
        // Calculate actual current week to compare
        const calculatedCurrentWeek = getCurrentWeekStart();
        const calculatedCurrentWeekDate = new Date(calculatedCurrentWeek + 'T00:00:00');
        
        // Check if this is the actual current calendar week
        const isCurrentWeek = weekStartDateObj.getTime() === calculatedCurrentWeekDate.getTime();
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const daysDiff = Math.floor((weekStartDateObj - today) / (1000 * 60 * 60 * 24));
        const isNextWeek = daysDiff > 0 && daysDiff <= 7;
        
        let weekLabel;
        if (isCurrentWeek) {
            weekLabel = `📅 Semana Actual - ${weekStartFormatted}`;
        } else if (isNextWeek) {
            weekLabel = `📅 Próxima Semana - ${weekStartFormatted}`;
        } else {
            weekLabel = `📅 Semana del ${weekStartFormatted}`;
        }
        
        let html = `
            <div style="background: rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 2rem; border: 1px solid rgba(255, 255, 255, 0.1);" class="shopping-week-container">
                <h3 style="font-family: 'Playfair Display', serif; color: var(--white); margin-bottom: 1.5rem; font-size: 1.5rem;" class="shopping-week-title">
                    ${weekLabel}
                </h3>
        `;
        
        const merged = mergeShoppingLists(weekMenuData);
        html += '<div id="shopping-summary-week"></div>';
        html += '<div id="shopping-categories-week"></div>';
        html += '</div>';
        
        display.innerHTML = html;
        
        // Store menu data for export functions
        currentShoppingMenuData = {
            menu_data: weekMenuData,
            week_start_date: weekStartDate,
            adults_count: window.familyComposition?.adults?.length || 0,
            children_count: window.familyComposition?.children?.length || 0
        };
        
        // Update summary
        updateShoppingSummary(weekMenuData, merged, 'week');
        
        // Render categories after DOM update
        const categoriesDiv = document.getElementById('shopping-categories-week');
        if (categoriesDiv) {
            renderShoppingCategories(merged, categoriesDiv);
        }
        
        // Show progress
        const progressContainer = document.getElementById('progress-container');
        if (progressContainer) {
            progressContainer.style.display = 'block';
        }
        updateShoppingProgress();
        
    } catch (error) {
        console.error('[ShoppingList] Error loading shopping list:', error);
        display.innerHTML = `
            <div class="empty-state">
                <h3>Error al cargar la lista de compra</h3>
                <p style="margin-top: 1rem; color: var(--silver);">
                    ${error.data?.error || error.message || 'Error desconocido'}
                </p>
                <button class="btn btn-primary" onclick="loadShoppingLists(getCurrentWeekStart())" style="margin-top: 1.5rem;">
                    Reintentar
                </button>
            </div>
        `;
    }
}

// Navigate shopping list to different week - same logic as navigateWeek
async function navigateShoppingWeek(direction) {
    console.log('[NavigateShoppingWeek] Navigating', direction, 'from week:', currentShoppingWeek);
    
    // If no current week, start from current week
    if (!currentShoppingWeek) {
        currentShoppingWeek = getCurrentWeekStart();
        console.log('[NavigateShoppingWeek] No current week, starting from:', currentShoppingWeek);
    }
    
    let targetWeekStart;
    
    if (direction === 'current') {
        // Go to current week
        targetWeekStart = getCurrentWeekStart();
        console.log('[NavigateShoppingWeek] Navigating to current week:', targetWeekStart);
    } else {
        // Navigate prev/next - use same logic as navigateWeek
        const currentDate = new Date(currentShoppingWeek + 'T00:00:00');
        let targetDate;
        
        if (direction === 'prev') {
            targetDate = new Date(currentDate);
            targetDate.setDate(targetDate.getDate() - 7);
        } else {
            // 'next'
            targetDate = new Date(currentDate);
            targetDate.setDate(targetDate.getDate() + 7);
        }
        
        // Ensure we get the Monday of the target week using local date components
        const targetMonday = getMondayOfWeek(targetDate);
        const mondayYear = targetMonday.getFullYear();
        const mondayMonth = targetMonday.getMonth();
        const mondayDate = targetMonday.getDate();
        targetWeekStart = `${mondayYear}-${String(mondayMonth + 1).padStart(2, '0')}-${String(mondayDate).padStart(2, '0')}`;
        console.log('[NavigateShoppingWeek] Navigating to:', targetWeekStart);
    }
    
    // Always update currentShoppingWeek to the target week
    currentShoppingWeek = targetWeekStart;
    updateShoppingWeekNavigation();
    
    // Load shopping list for that week
    await loadShoppingLists(targetWeekStart);
}

// Update shopping week navigation display
function updateShoppingWeekNavigation() {
    const navContainer = document.getElementById('shopping-week-navigation');
    if (!navContainer) return;
    
    if (!currentShoppingWeek) {
        currentShoppingWeek = getCurrentWeekStart();
    }
    
    // Format week display nicely - same logic as updateWeekNavigation
    const weekDate = formatWeekStart(currentShoppingWeek);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const weekStart = new Date(currentShoppingWeek + 'T00:00:00');
    weekStart.setHours(0, 0, 0, 0);
    
    // Calculate actual current week to compare
    const calculatedCurrentWeek = getCurrentWeekStart();
    const calculatedCurrentWeekDate = new Date(calculatedCurrentWeek + 'T00:00:00');
    
    // Check if this is the actual current calendar week
    const isCurrentWeek = weekStart.getTime() === calculatedCurrentWeekDate.getTime();
    const daysDiff = Math.floor((weekStart - today) / (1000 * 60 * 60 * 24));
    const isNextWeek = daysDiff > 0 && daysDiff <= 7; // Next week
    
    let weekLabel;
    if (isCurrentWeek) {
        weekLabel = `<span style="color: var(--gold);">📅 Semana Actual</span><br><span style="font-size: 0.9rem; color: var(--silver);">${weekDate}</span>`;
    } else if (isNextWeek) {
        weekLabel = `<span style="color: var(--sage);">📅 Próxima Semana</span><br><span style="font-size: 0.9rem; color: var(--silver);">${weekDate}</span>`;
    } else {
        weekLabel = `📅 Semana del ${weekDate}`;
    }
    
    navContainer.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <button 
                class="btn btn-secondary" 
                onclick="navigateShoppingWeek('prev')"
                style="padding: 0.75rem 1.5rem; min-width: 120px;"
            >
                ← Anterior
            </button>
            <div style="font-size: 1.2rem; color: var(--white); font-weight: 600; text-align: center; flex: 1;">
                ${weekLabel}
            </div>
            <button 
                class="btn btn-secondary" 
                onclick="navigateShoppingWeek('next')"
                style="padding: 0.75rem 1.5rem; min-width: 120px;"
            >
                Siguiente →
            </button>
        </div>
        <div style="text-align: center; margin-top: 1rem;">
            <button class="btn btn-primary" onclick="navigateShoppingWeek('current')" style="padding: 0.5rem 1.5rem; font-size: 0.9rem;">
                📅 Ver Semana Actual
            </button>
        </div>
    `;
}

// Load family composition
async function loadFamilyComposition() {
    try {
        const adultsResult = await API.get('/api/adults');
        const childrenResult = await API.get('/api/children');
        
        const adults = adultsResult.data || [];
        const children = childrenResult.data || [];
        
        renderFamilyComposition(adults, children);
    } catch (error) {
        console.error('[ShoppingList] Error loading family composition:', error);
    }
}

// Render family composition
function renderFamilyComposition(adults, children) {
    const familyCard = document.getElementById('family-composition-card');
    const compositionGrid = document.getElementById('family-composition-grid');
    
    if (adults.length === 0 && children.length === 0) {
        familyCard.style.display = 'none';
        return;
    }
    
    familyCard.style.display = 'block';
    
    const totalPeople = adults.length + children.length;
    const childrenAges = children.map(c => c.edad || 'N/A').filter(a => a !== 'N/A').join(', ');
    
    compositionGrid.innerHTML = `
        <div>
            <div style="font-family: 'Playfair Display', serif; font-size: 2rem; color: var(--gold); margin-bottom: 0.25rem;">${totalPeople}</div>
            <div style="color: var(--silver); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Total People</div>
        </div>
        <div>
            <div style="font-family: 'Playfair Display', serif; font-size: 2rem; color: var(--gold); margin-bottom: 0.25rem;">${adults.length}</div>
            <div style="color: var(--silver); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Adults</div>
        </div>
        <div>
            <div style="font-family: 'Playfair Display', serif; font-size: 2rem; color: var(--gold); margin-bottom: 0.25rem;">${children.length}</div>
            <div style="color: var(--silver); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Children</div>
        </div>
        ${children.length > 0 && childrenAges ? `
            <div>
                <div style="font-family: 'Playfair Display', serif; font-size: 1.5rem; color: var(--gold); margin-bottom: 0.25rem;">${childrenAges}</div>
                <div style="color: var(--silver); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Ages (years)</div>
            </div>
        ` : ''}
    `;
}

// Extract ingredients directly from menu meals
function extractIngredientsFromMenu(menuData) {
    console.log('[ShoppingList] Extracting ingredients from menu meals...');
    const ingredientsMap = {};
    const numAdults = currentShoppingMenuData?.adults_count || 2;
    const numChildren = currentShoppingMenuData?.children_count || 0;
    
    // Count meals per type to adjust quantities
    const mealCounts = {
        adults: { desayuno: 0, comida: 0, cena: 0, merienda: 0 },
        children: { desayuno: 0, comida: 0, cena: 0, merienda: 0 }
    };
    
    // Extract from adults menu
    if (menuData.menu_adultos && menuData.menu_adultos.dias) {
        Object.values(menuData.menu_adultos.dias).forEach(day => {
            ['desayuno', 'comida', 'cena'].forEach(mealType => {
                if (day[mealType] && day[mealType].ingredientes) {
                    mealCounts.adults[mealType]++;
                    const ingredients = Array.isArray(day[mealType].ingredientes) 
                        ? day[mealType].ingredientes 
                        : [];
                    
                    ingredients.forEach(ingredient => {
                        const ingName = typeof ingredient === 'string' ? ingredient : (ingredient.nombre || ingredient.name || String(ingredient));
                        const normalizedName = ingName.toLowerCase().trim();
                        
                        if (!ingredientsMap[normalizedName]) {
                            ingredientsMap[normalizedName] = {
                                nombre: ingName,
                                count: 0,
                                meals: { adults: { desayuno: 0, comida: 0, cena: 0 }, children: { desayuno: 0, comida: 0, cena: 0, merienda: 0 } }
                            };
                        }
                        ingredientsMap[normalizedName].count++;
                        ingredientsMap[normalizedName].meals.adults[mealType]++;
                    });
                }
            });
        });
    }
    
    // Extract from children menu
    if (menuData.menu_ninos && menuData.menu_ninos.dias) {
        Object.values(menuData.menu_ninos.dias).forEach(day => {
            ['desayuno', 'comida', 'merienda', 'cena'].forEach(mealType => {
                if (day[mealType] && day[mealType].ingredientes) {
                    mealCounts.children[mealType]++;
                    const ingredients = Array.isArray(day[mealType].ingredientes) 
                        ? day[mealType].ingredientes 
                        : [];
                    
                    ingredients.forEach(ingredient => {
                        const ingName = typeof ingredient === 'string' ? ingredient : (ingredient.nombre || ingredient.name || String(ingredient));
                        const normalizedName = ingName.toLowerCase().trim();
                        
                        if (!ingredientsMap[normalizedName]) {
                            ingredientsMap[normalizedName] = {
                                nombre: ingName,
                                count: 0,
                                meals: { adults: { desayuno: 0, comida: 0, cena: 0 }, children: { desayuno: 0, comida: 0, cena: 0, merienda: 0 } }
                            };
                        }
                        ingredientsMap[normalizedName].count++;
                        ingredientsMap[normalizedName].meals.children[mealType]++;
                    });
                }
            });
        });
    }
    
    console.log('[ShoppingList] Meal counts:', mealCounts);
    console.log('[ShoppingList] Extracted ingredients:', Object.keys(ingredientsMap).length);
    
    // Categorize and estimate quantities based on meal counts
    const categorized = {
        'frutas_verduras': [],
        'carnes_pescados': [],
        'lacteos_huevos': [],
        'cereales_legumbres': [],
        'despensa': [],
        'congelados': [],
        'otros': []
    };
    
    Object.values(ingredientsMap).forEach(ing => {
        const category = categorizeIngredient(ing.nombre);
        
        // Calculate quantity based on how many times it appears and meal types
        const quantity = calculateQuantityFromMeals(
            ing.nombre, 
            ing.meals, 
            mealCounts, 
            numAdults, 
            numChildren
        );
        
        categorized[category].push({
            nombre: ing.nombre,
            cantidad: quantity,
            notas: ''
        });
    });
    
    // Remove empty categories
    Object.keys(categorized).forEach(cat => {
        if (categorized[cat].length === 0) {
            delete categorized[cat];
        }
    });
    
    return categorized;
}

// Categorize a single ingredient
function categorizeIngredient(ingredientName) {
    const ingLower = ingredientName.toLowerCase();
    
    if (ingLower.includes('tomate') || ingLower.includes('tomato') || ingLower.includes('lechuga') || ingLower.includes('lettuce') || 
        ingLower.includes('zanahoria') || ingLower.includes('carrot') || ingLower.includes('cebolla') || ingLower.includes('onion') || 
        ingLower.includes('ajo') || ingLower.includes('garlic') || ingLower.includes('pimiento') || ingLower.includes('pepper') || 
        ingLower.includes('calabacín') || ingLower.includes('zucchini') || ingLower.includes('brócoli') || ingLower.includes('broccoli') || 
        ingLower.includes('coliflor') || ingLower.includes('cauliflower') || ingLower.includes('patata') || ingLower.includes('potato') ||
        ingLower.includes('verdura') || ingLower.includes('vegetable') || ingLower.includes('fruta') || ingLower.includes('fruit')) {
        return 'frutas_verduras';
    } else if (ingLower.includes('pollo') || ingLower.includes('chicken') || ingLower.includes('cerdo') || ingLower.includes('pork') || 
               ingLower.includes('ternera') || ingLower.includes('beef') || ingLower.includes('carne') || ingLower.includes('meat') || 
               ingLower.includes('pescado') || ingLower.includes('fish') || ingLower.includes('salmón') || ingLower.includes('salmon') ||
               ingLower.includes('merluza') || ingLower.includes('hake') || ingLower.includes('bacalao') || ingLower.includes('cod') ||
               ingLower.includes('gambas') || ingLower.includes('shrimp') || ingLower.includes('mejillones') || ingLower.includes('mussels')) {
        return 'carnes_pescados';
    } else if (ingLower.includes('huevo') || ingLower.includes('egg') || ingLower.includes('leche') || ingLower.includes('milk') || 
               ingLower.includes('queso') || ingLower.includes('cheese') || ingLower.includes('mantequilla') || ingLower.includes('butter')) {
        return 'lacteos_huevos';
    } else if (ingLower.includes('arroz') || ingLower.includes('rice') || ingLower.includes('pasta') || ingLower.includes('harina') || 
               ingLower.includes('flour') || ingLower.includes('pan') || ingLower.includes('bread') || ingLower.includes('quinoa') ||
               ingLower.includes('legumbre') || ingLower.includes('legume')) {
        return 'cereales_legumbres';
    } else if (ingLower.includes('congelado') || ingLower.includes('frozen')) {
        return 'congelados';
    } else {
        return 'despensa';
    }
}

// Calculate quantity based on meal counts
function calculateQuantityFromMeals(ingredientName, meals, mealCounts, numAdults, numChildren) {
    const ingLower = ingredientName.toLowerCase();
    const totalAdultsMeals = mealCounts.adults.desayuno + mealCounts.adults.comida + mealCounts.adults.cena;
    const totalChildrenMeals = mealCounts.children.desayuno + mealCounts.children.comida + mealCounts.children.cena + mealCounts.children.merienda;
    
    // Count how many times this ingredient appears in each meal type
    const adultMealOccurrences = meals.adults.desayuno + meals.adults.comida + meals.adults.cena;
    const childMealOccurrences = meals.children.desayuno + meals.children.comida + meals.children.cena + meals.children.merienda;
    
    // Base quantity per person per meal
    let basePerPersonPerMeal = 0;
    
    // Protein estimates
    if (ingLower.includes('pollo') || ingLower.includes('chicken') || ingLower.includes('pavo') || ingLower.includes('turkey')) {
        basePerPersonPerMeal = 150; // grams per person per meal
    } else if (ingLower.includes('cerdo') || ingLower.includes('pork') || ingLower.includes('ternera') || ingLower.includes('beef') || ingLower.includes('carne') || ingLower.includes('meat')) {
        basePerPersonPerMeal = 120;
    } else if (ingLower.includes('pescado') || ingLower.includes('fish') || ingLower.includes('salmón') || ingLower.includes('salmon') || ingLower.includes('merluza') || ingLower.includes('hake') || ingLower.includes('bacalao') || ingLower.includes('cod') || ingLower.includes('gambas') || ingLower.includes('shrimp') || ingLower.includes('mejillones') || ingLower.includes('mussels')) {
        basePerPersonPerMeal = 130;
    } else if (ingLower.includes('huevo') || ingLower.includes('egg')) {
        const totalEggs = Math.ceil((adultMealOccurrences * numAdults + childMealOccurrences * numChildren) * 1.5);
        if (totalEggs === 0) return '';
        return `${totalEggs} unidades`;
    }
    // Vegetables
    else if (ingLower.includes('tomate') || ingLower.includes('tomato') || ingLower.includes('cebolla') || ingLower.includes('onion') || ingLower.includes('ajo') || ingLower.includes('garlic') || ingLower.includes('pimiento') || ingLower.includes('pepper') || ingLower.includes('calabacín') || ingLower.includes('zucchini')) {
        basePerPersonPerMeal = 80;
    } else if (ingLower.includes('lechuga') || ingLower.includes('lettuce') || ingLower.includes('brócoli') || ingLower.includes('broccoli') || ingLower.includes('coliflor') || ingLower.includes('cauliflower')) {
        basePerPersonPerMeal = 60;
    } else if (ingLower.includes('zanahoria') || ingLower.includes('carrot') || ingLower.includes('patata') || ingLower.includes('potato')) {
        basePerPersonPerMeal = 100;
    }
    // Dairy
    else if (ingLower.includes('leche') || ingLower.includes('milk')) {
        const totalLiters = Math.ceil((adultMealOccurrences * numAdults + childMealOccurrences * numChildren) * 0.2);
        if (totalLiters === 0) return '';
        return `${totalLiters} l`;
    } else if (ingLower.includes('queso') || ingLower.includes('cheese') || ingLower.includes('mantequilla') || ingLower.includes('butter')) {
        basePerPersonPerMeal = 30;
    }
    // Grains
    else if (ingLower.includes('arroz') || ingLower.includes('rice') || ingLower.includes('pasta') || ingLower.includes('harina') || ingLower.includes('flour') || ingLower.includes('pan') || ingLower.includes('bread') || ingLower.includes('quinoa')) {
        basePerPersonPerMeal = 100;
    }
    // Oils and condiments
    else if (ingLower.includes('aceite') || ingLower.includes('oil')) {
        const totalLiters = Math.ceil((adultMealOccurrences * numAdults + childMealOccurrences * numChildren) * 0.015);
        if (totalLiters === 0) return '';
        return `${totalLiters} l`;
    } else {
        basePerPersonPerMeal = 50; // Default
    }
    
    if (basePerPersonPerMeal > 0) {
        const totalGrams = Math.ceil((adultMealOccurrences * numAdults + childMealOccurrences * numChildren) * basePerPersonPerMeal);
        // Don't return zero quantities
        if (totalGrams === 0) {
            return '';
        }
        if (totalGrams >= 1000) {
            return `${(totalGrams / 1000).toFixed(2).replace(/\.?0+$/, '')} kg`;
        } else {
            return `${totalGrams}g`;
        }
    }
    
    const totalOccurrences = adultMealOccurrences + childMealOccurrences;
    // Don't return zero quantities
    if (totalOccurrences === 0) {
        return '';
    }
    return `${totalOccurrences} unidades`;
}

// Merge shopping lists from adults and children
function mergeShoppingLists(menuData) {
    console.log('[ShoppingList] Merging shopping lists...');
    const merged = {};
    
    // Get family size for quantity estimation
    const numAdults = currentShoppingMenuData?.adults_count || 2;
    const numChildren = currentShoppingMenuData?.children_count || 0;
    
    // FIRST: Try to extract ingredients directly from menu meals
    const extractedIngredients = extractIngredientsFromMenu(menuData);
    
    if (Object.keys(extractedIngredients).length > 0) {
        console.log('[ShoppingList] Using ingredients extracted from menu meals');
        // Merge items by name within each category
        Object.entries(extractedIngredients).forEach(([category, items]) => {
            const itemsMap = {};
            items.forEach(item => {
                const normalizedName = item.nombre.toLowerCase().trim();
                const existingKey = Object.keys(itemsMap).find(key => key.toLowerCase().trim() === normalizedName);
                
                if (existingKey) {
                    const combinedQty = combineQuantities(itemsMap[existingKey].cantidad, item.cantidad);
                    // Only update if combined quantity is not empty
                    if (combinedQty && combinedQty.trim()) {
                        itemsMap[existingKey].cantidad = combinedQty;
                    } else {
                        // If combined is empty, remove the item
                        delete itemsMap[existingKey];
                    }
                } else {
                    // Only add if quantity is not empty or zero
                    const cantidad = item.cantidad || '';
                    if (cantidad && cantidad.trim()) {
                        const cantidadLower = cantidad.toLowerCase().trim();
                        if (cantidadLower !== '0' && cantidadLower !== '0g' && cantidadLower !== '0 g' &&
                            cantidadLower !== '0kg' && cantidadLower !== '0 kg' && cantidadLower !== '0ml' &&
                            cantidadLower !== '0 ml' && cantidadLower !== '0l' && cantidadLower !== '0 l' &&
                            cantidadLower !== '0 unidades' && cantidadLower !== '0unidades') {
                            itemsMap[item.nombre] = item;
                        }
                    }
                }
            });
            // Filter out items with empty quantities before adding to merged
            merged[category] = Object.values(itemsMap).filter(item => {
                const cantidad = item.cantidad || '';
                if (!cantidad || !cantidad.trim()) return false;
                const cantidadLower = cantidad.toLowerCase().trim();
                return cantidadLower !== '0' && cantidadLower !== '0g' && cantidadLower !== '0 g' &&
                       cantidadLower !== '0kg' && cantidadLower !== '0 kg' && cantidadLower !== '0ml' &&
                       cantidadLower !== '0 ml' && cantidadLower !== '0l' && cantidadLower !== '0 l' &&
                       cantidadLower !== '0 unidades' && cantidadLower !== '0unidades';
            });
        });
        
        console.log('[ShoppingList] Merged result from extracted ingredients:', Object.keys(merged));
        return merged;
    }
    
    // FALLBACK: Try new structure first (por_categoria)
    let adultList = menuData.menu_adultos?.lista_compras?.por_categoria || {};
    let childrenList = menuData.menu_ninos?.lista_compras?.por_categoria || {};
    
    console.log('[ShoppingList] Adult list (por_categoria):', Object.keys(adultList));
    console.log('[ShoppingList] Children list (por_categoria):', Object.keys(childrenList));
    
    // If no por_categoria, try old structure (array)
    if (Object.keys(adultList).length === 0 && Array.isArray(menuData.menu_adultos?.lista_compras)) {
        console.log('[ShoppingList] Using old array format for adults, converting...');
        const adultArray = menuData.menu_adultos.lista_compras;
        adultList = categorizeShoppingItems(adultArray, numAdults, 0);
    }
    
    if (Object.keys(childrenList).length === 0 && Array.isArray(menuData.menu_ninos?.lista_compras)) {
        console.log('[ShoppingList] Using old array format for children, converting...');
        const childrenArray = menuData.menu_ninos.lista_compras;
        childrenList = categorizeShoppingItems(childrenArray, 0, numChildren);
    }
    
    // Also check for lista_compras_combinada at root level
    if (Object.keys(adultList).length === 0 && Object.keys(childrenList).length === 0) {
        if (Array.isArray(menuData.lista_compras_combinada)) {
            console.log('[ShoppingList] Using lista_compras_combinada array format...');
            const combinedArray = menuData.lista_compras_combinada;
            adultList = categorizeShoppingItems(combinedArray, numAdults, numChildren);
            childrenList = {}; // Empty since it's already combined
        } else if (menuData.lista_compras_combinada && typeof menuData.lista_compras_combinada === 'object') {
            console.log('[ShoppingList] Using lista_compras_combinada object format...');
            adultList = menuData.lista_compras_combinada.por_categoria || menuData.lista_compras_combinada;
        }
        
        // Also check for old lista_compras at root
        if (Object.keys(adultList).length === 0 && Array.isArray(menuData.lista_compras)) {
            console.log('[ShoppingList] Using root lista_compras array format...');
            adultList = categorizeShoppingItems(menuData.lista_compras, numAdults, numChildren);
        }
    }
    
    console.log('[ShoppingList] Final adult list categories:', Object.keys(adultList));
    console.log('[ShoppingList] Final children list categories:', Object.keys(childrenList));
    
    const allCategories = new Set([
        ...Object.keys(adultList),
        ...Object.keys(childrenList)
    ]);
    
    allCategories.forEach(category => {
        const adultItems = Array.isArray(adultList[category]) ? adultList[category] : [];
        const childrenItems = Array.isArray(childrenList[category]) ? childrenList[category] : [];
        
        // Merge items by name
        const itemsMap = {};
        
        [...adultItems, ...childrenItems].forEach(item => {
            // Handle both object format and string format
            let itemName, itemQuantity, itemNotes;
            
            if (typeof item === 'string') {
                itemName = item;
                itemQuantity = '';
                itemNotes = '';
            } else {
                itemName = item.nombre || item.name || String(item);
                // Try multiple possible quantity fields
                itemQuantity = item.cantidad || item.quantity || item.amount || item.cantidad_necesaria || '';
                itemNotes = item.notas || item.notes || item.descripcion || '';
            }
            
            // Normalize item name (remove extra spaces, lowercase for comparison)
            const normalizedName = itemName.toLowerCase().trim();
            
            // Check if we already have this item (case-insensitive)
            const existingKey = Object.keys(itemsMap).find(key => key.toLowerCase().trim() === normalizedName);
            
            if (existingKey) {
                // Combine quantities
                itemsMap[existingKey].cantidad = combineQuantities(
                    itemsMap[existingKey].cantidad,
                    itemQuantity
                );
                // Merge notes
                if (itemNotes && !itemsMap[existingKey].notas) {
                    itemsMap[existingKey].notas = itemNotes;
                }
            } else {
                // Only add if quantity is not empty or zero
                const cantidad = itemQuantity || '';
                if (cantidad && cantidad.trim()) {
                    const cantidadLower = cantidad.toLowerCase().trim();
                    if (cantidadLower !== '0' && cantidadLower !== '0g' && cantidadLower !== '0 g' &&
                        cantidadLower !== '0kg' && cantidadLower !== '0 kg' && cantidadLower !== '0ml' &&
                        cantidadLower !== '0 ml' && cantidadLower !== '0l' && cantidadLower !== '0 l' &&
                        cantidadLower !== '0 unidades' && cantidadLower !== '0unidades') {
                        itemsMap[itemName] = {
                            nombre: itemName,
                            cantidad: itemQuantity,
                            notas: itemNotes
                        };
                    }
                }
            }
        });
        
        // Filter out items with empty or zero quantities
        merged[category] = Object.values(itemsMap).filter(item => {
            const cantidad = item.cantidad || '';
            if (!cantidad || !cantidad.trim()) return false;
            const cantidadLower = cantidad.toLowerCase().trim();
            return cantidadLower !== '0' && cantidadLower !== '0g' && cantidadLower !== '0 g' &&
                   cantidadLower !== '0kg' && cantidadLower !== '0 kg' && cantidadLower !== '0ml' &&
                   cantidadLower !== '0 ml' && cantidadLower !== '0l' && cantidadLower !== '0 l' &&
                   cantidadLower !== '0 unidades' && cantidadLower !== '0unidades';
        });
    });
    
    console.log('[ShoppingList] Merged result:', Object.keys(merged), 'with', Object.values(merged).reduce((sum, items) => sum + items.length, 0), 'total items');
    return merged;
}

// Estimate quantity based on item name and family size
function estimateQuantityForItem(itemName, category, numAdults, numChildren) {
    const itemLower = itemName.toLowerCase();
    const totalPeople = numAdults + numChildren;
    
    // Protein estimates (per person per week)
    if (itemLower.includes('pollo') || itemLower.includes('chicken') || itemLower.includes('pavo') || itemLower.includes('turkey')) {
        return `${totalPeople * 200}g`;
    } else if (itemLower.includes('cerdo') || itemLower.includes('pork') || itemLower.includes('ternera') || itemLower.includes('beef') || itemLower.includes('carne') || itemLower.includes('meat')) {
        return `${totalPeople * 150}g`;
    } else if (itemLower.includes('pescado') || itemLower.includes('fish') || itemLower.includes('salmón') || itemLower.includes('salmon') || itemLower.includes('merluza') || itemLower.includes('hake') || itemLower.includes('bacalao') || itemLower.includes('cod') || itemLower.includes('gambas') || itemLower.includes('shrimp') || itemLower.includes('mejillones') || itemLower.includes('mussels')) {
        return `${totalPeople * 150}g`;
    } else if (itemLower.includes('huevo') || itemLower.includes('egg')) {
        return `${totalPeople * 6} unidades`;
    }
    
    // Vegetables (per person per week)
    else if (itemLower.includes('tomate') || itemLower.includes('tomato') || itemLower.includes('cebolla') || itemLower.includes('onion') || itemLower.includes('ajo') || itemLower.includes('garlic') || itemLower.includes('pimiento') || itemLower.includes('pepper') || itemLower.includes('calabacín') || itemLower.includes('zucchini')) {
        return `${totalPeople * 500}g`;
    } else if (itemLower.includes('lechuga') || itemLower.includes('lettuce') || itemLower.includes('espinaca') || itemLower.includes('spinach') || itemLower.includes('brócoli') || itemLower.includes('broccoli') || itemLower.includes('coliflor') || itemLower.includes('cauliflower')) {
        return `${totalPeople * 300}g`;
    } else if (itemLower.includes('zanahoria') || itemLower.includes('carrot') || itemLower.includes('patata') || itemLower.includes('potato') || itemLower.includes('papas')) {
        return `${totalPeople * 1} kg`;
    }
    
    // Dairy
    else if (itemLower.includes('leche') || itemLower.includes('milk') || itemLower.includes('queso') || itemLower.includes('cheese') || itemLower.includes('mantequilla') || itemLower.includes('butter')) {
        return itemLower.includes('leche') || itemLower.includes('milk') ? `${totalPeople * 500}ml` : `${totalPeople * 200}g`;
    }
    
    // Grains
    else if (itemLower.includes('arroz') || itemLower.includes('rice') || itemLower.includes('pasta') || itemLower.includes('harina') || itemLower.includes('flour') || itemLower.includes('pan') || itemLower.includes('bread') || itemLower.includes('quinoa')) {
        return `${totalPeople * 500}g`;
    }
    
    // Oils and condiments
    else if (itemLower.includes('aceite') || itemLower.includes('oil') || itemLower.includes('vinagre') || itemLower.includes('vinegar') || itemLower.includes('salsa') || itemLower.includes('sauce')) {
        return itemLower.includes('aceite') || itemLower.includes('oil') ? `${totalPeople * 250}ml` : `${totalPeople * 200}ml`;
    }
    
    // Default
    return `${totalPeople * 200}g`;
}

// Categorize shopping items from array format
function categorizeShoppingItems(items, numAdults = 0, numChildren = 0) {
    const categorized = {
        'frutas_verduras': [],
        'carnes_pescados': [],
        'lacteos_huevos': [],
        'cereales_legumbres': [],
        'despensa': [],
        'congelados': [],
        'otros': []
    };
    
    // Keywords for categorization
    const categoryKeywords = {
        'frutas_verduras': ['tomate', 'tomates', 'lechuga', 'zanahoria', 'zanahorias', 'cebolla', 'cebollas', 'ajo', 'pimiento', 'pimientos', 'calabacín', 'calabacines', 'brócoli', 'espinaca', 'espinacas', 'manzana', 'manzanas', 'plátano', 'plátanos', 'naranja', 'naranjas', 'limón', 'limones', 'verdura', 'verduras', 'fruta', 'frutas', 'ensalada', 'pepino', 'pepinos'],
        'carnes_pescados': ['pollo', 'cerdo', 'ternera', 'salmón', 'atún', 'pescado', 'pescados', 'carne', 'carnes', 'pavo', 'jamón', 'chorizo', 'filete', 'filetes', 'solomillo', 'pechuga'],
        'lacteos_huevos': ['huevo', 'huevos', 'leche', 'queso', 'quesos', 'yogur', 'yogures', 'mantequilla', 'nata', 'lácteo', 'lácteos'],
        'cereales_legumbres': ['arroz', 'pasta', 'pan', 'harina', 'lenteja', 'lentejas', 'garbanzo', 'garbanzos', 'judía', 'judías', 'avena', 'cereal', 'cereales', 'legumbre', 'legumbres'],
        'despensa': ['aceite', 'sal', 'azúcar', 'vinagre', 'especia', 'especias', 'condimento', 'condimentos', 'salsa', 'salsas', 'caldo', 'caldos'],
        'congelados': ['congelado', 'congelados', 'helado', 'helados'],
        'otros': []
    };
    
    items.forEach(item => {
        const itemStr = typeof item === 'string' ? item.toLowerCase() : (item.nombre || item.name || '').toLowerCase();
        let categorized_flag = false;
        
        for (const [category, keywords] of Object.entries(categoryKeywords)) {
            if (keywords.some(keyword => itemStr.includes(keyword))) {
                if (typeof item === 'string') {
                    categorized[category].push({ 
                        nombre: item, 
                        cantidad: estimateQuantityForItem(item, category, numAdults, numChildren), 
                        notas: '' 
                    });
                } else {
                    // If it's already an object but doesn't have cantidad, estimate it
                    if (!item.cantidad && !item.quantity) {
                        item.cantidad = estimateQuantityForItem(item.nombre || item.name || item, category, numAdults, numChildren);
                    }
                    categorized[category].push(item);
                }
                categorized_flag = true;
                break;
            }
        }
        
        if (!categorized_flag) {
            if (typeof item === 'string') {
                categorized['otros'].push({ 
                    nombre: item, 
                    cantidad: estimateQuantityForItem(item, 'otros', numAdults, numChildren), 
                    notas: '' 
                });
            } else {
                // If it's already an object but doesn't have cantidad, estimate it
                if (!item.cantidad && !item.quantity) {
                    item.cantidad = estimateQuantityForItem(item.nombre || item.name || item, 'otros', numAdults, numChildren);
                }
                categorized['otros'].push(item);
            }
        }
    });
    
    // Remove empty categories
    Object.keys(categorized).forEach(cat => {
        if (categorized[cat].length === 0) {
            delete categorized[cat];
        }
    });
    
    return categorized;
}

// Combine quantities by parsing and summing
function combineQuantities(q1, q2) {
    // Handle empty or zero quantities
    if (!q2 || !q2.trim() || q2.trim() === '0' || q2.trim().toLowerCase() === '0g' || q2.trim().toLowerCase() === '0 g') {
        return q1 || '';
    }
    if (!q1 || !q1.trim() || q1.trim() === '0' || q1.trim().toLowerCase() === '0g' || q1.trim().toLowerCase() === '0 g') {
        return q2 || '';
    }
    if (q1 === q2) return q1;
    
    // Parse quantities
    const parseQuantity = (q) => {
        if (!q || typeof q !== 'string') return null;
        
        const qLower = q.toLowerCase().trim();
        
        // Skip zero quantities
        if (qLower === '0' || qLower === '0g' || qLower === '0 g' || qLower === '0kg' || qLower === '0 kg' || 
            qLower === '0ml' || qLower === '0 ml' || qLower === '0l' || qLower === '0 l' || 
            qLower === '0 unidades' || qLower === '0unidades') {
            return null;
        }
        
        // Extract number and unit
        const match = qLower.match(/^([\d.]+)\s*(kg|g|ml|l|litro|litros|unidades?|unidad|piezas?|pieza|ud|uds)?/);
        if (!match) return null;
        
        let value = parseFloat(match[1]);
        
        // Skip zero values
        if (value === 0) return null;
        
        let unit = (match[2] || '').trim();
        
        // Normalize units
        if (unit === 'kg' || unit === 'kilogramo' || unit === 'kilogramos') {
            return { value: value * 1000, unit: 'g', originalUnit: 'kg' };
        } else if (unit === 'l' || unit === 'litro' || unit === 'litros') {
            return { value: value * 1000, unit: 'ml', originalUnit: 'l' };
        } else if (unit === 'unidad' || unit === 'unidades' || unit === 'ud' || unit === 'uds' || unit === 'pieza' || unit === 'piezas') {
            return { value: value, unit: 'unidades', originalUnit: 'unidades' };
        } else if (unit === 'g' || unit === 'gramo' || unit === 'gramos') {
            return { value: value, unit: 'g', originalUnit: 'g' };
        } else if (unit === 'ml' || unit === 'mililitro' || unit === 'mililitros') {
            return { value: value, unit: 'ml', originalUnit: 'ml' };
        } else {
            // Default: assume grams if no unit specified
            return { value: value, unit: 'g', originalUnit: 'g' };
        }
    };
    
    const parsed1 = parseQuantity(q1);
    const parsed2 = parseQuantity(q2);
    
    // If both are null (zero or invalid), return empty
    if (!parsed1 && !parsed2) {
        return '';
    }
    
    // If one is null (zero), return the other
    if (!parsed1) return q2;
    if (!parsed2) return q1;
    
    // If units don't match, concatenate
    if (parsed1.unit !== parsed2.unit) {
        return `${q1} + ${q2}`;
    }
    
    // Sum values
    const totalValue = parsed1.value + parsed2.value;
    
    // Don't return zero values
    if (totalValue === 0) {
        return '';
    }
    
    // Format result based on unit
    if (parsed1.unit === 'unidades') {
        return `${Math.round(totalValue)} unidades`;
    } else if (parsed1.unit === 'g') {
        if (totalValue >= 1000) {
            return `${(totalValue / 1000).toFixed(2).replace(/\.?0+$/, '')} kg`;
        } else {
            return `${Math.round(totalValue)}g`;
        }
    } else if (parsed1.unit === 'ml') {
        if (totalValue >= 1000) {
            return `${(totalValue / 1000).toFixed(2).replace(/\.?0+$/, '')} l`;
        } else {
            return `${Math.round(totalValue)}ml`;
        }
    }
    
    return `${totalValue} ${parsed1.unit}`;
}

// Update shopping summary
function updateShoppingSummary(menuData, categories, suffix = 'week') {
    // Calculate total items
    let totalItems = 0;
    Object.values(categories).forEach(items => {
        totalItems += items.length;
    });
    
    const summaryDiv = document.getElementById(`shopping-summary${suffix ? '-' + suffix : ''}`);
    if (!summaryDiv) {
        // Fallback to old summary card if new div doesn't exist
        const summaryCard = document.getElementById('summary-card');
        if (summaryCard) {
            summaryCard.style.display = 'block';
            shoppingTotalItems = totalItems;
            const totalItemsEl = document.getElementById('total-items-summary');
            if (totalItemsEl) totalItemsEl.textContent = totalItems;
            const adultSummary = menuData.menu_adultos?.lista_compras?.resumen_cantidades || {};
            const childrenSummary = menuData.menu_ninos?.lista_compras?.resumen_cantidades || {};
            const totalWeightEl = document.getElementById('total-weight-summary');
            if (totalWeightEl) totalWeightEl.textContent = adultSummary.peso_aproximado || childrenSummary.peso_aproximado || '-';
            const totalBudgetEl = document.getElementById('total-budget-summary');
            if (totalBudgetEl) totalBudgetEl.textContent = adultSummary.presupuesto_estimado || '-';
            const weekDateEl = document.getElementById('week-date-summary');
            if (weekDateEl) weekDateEl.textContent = menuData.semana || '-';
        }
        return;
    }
    
    // Build summary HTML
    const adultSummary = menuData.menu_adultos?.lista_compras?.resumen_cantidades || {};
    const childrenSummary = menuData.menu_ninos?.lista_compras?.resumen_cantidades || {};
    const weekDate = menuData.semana || '-';
    
    summaryDiv.innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem;">
            <div style="text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.03); border-radius: 12px;">
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--gold);">${totalItems}</div>
                <div style="color: var(--silver); font-size: 0.85rem; margin-top: 0.5rem;">Total Items</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.03); border-radius: 12px;">
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--gold);">${adultSummary.peso_aproximado || childrenSummary.peso_aproximado || '-'}</div>
                <div style="color: var(--silver); font-size: 0.85rem; margin-top: 0.5rem;">Peso Aprox.</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.03); border-radius: 12px;">
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--gold);">${adultSummary.presupuesto_estimado || '-'}</div>
                <div style="color: var(--silver); font-size: 0.85rem; margin-top: 0.5rem;">Presupuesto</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.03); border-radius: 12px;">
                <div style="font-size: 1rem; font-weight: 500; color: var(--gold);">${weekDate}</div>
                <div style="color: var(--silver); font-size: 0.85rem; margin-top: 0.5rem;">Semana</div>
            </div>
        </div>
    `;
}

// Render shopping categories
function renderShoppingCategories(categories, display) {
    display.innerHTML = '';
    
    const totalItems = Object.values(categories).reduce((sum, items) => sum + items.length, 0);
    
    if (totalItems === 0) {
        display.innerHTML = `
            <div class="empty-state">
                <h3>No hay lista de compra disponible</h3>
                <p style="margin-top: 1rem; color: var(--silver);">
                    Este menú no incluye una lista de compra. Genera un nuevo menú para obtener una lista de compra completa.
                </p>
            </div>
        `;
        return;
    }
    
    Object.entries(categories).forEach(([category, items]) => {
        // Filter out items with empty or zero quantities
        const validItems = items.filter(item => {
            const cantidad = item.cantidad || item.quantity || '';
            if (!cantidad || !cantidad.trim()) return false;
            const cantidadLower = cantidad.toLowerCase().trim();
            // Filter out zero quantities
            if (cantidadLower === '0' || cantidadLower === '0g' || cantidadLower === '0 g' || 
                cantidadLower === '0kg' || cantidadLower === '0 kg' || cantidadLower === '0ml' || 
                cantidadLower === '0 ml' || cantidadLower === '0l' || cantidadLower === '0 l' ||
                cantidadLower === '0 unidades' || cantidadLower === '0unidades') {
                return false;
            }
            return true;
        });
        
        if (validItems.length === 0) return;
        
        const categoryName = shoppingCategoryNames[category] || category;
        const icon = shoppingCategoryIcons[category] || '📦';
        
        const section = document.createElement('div');
        section.style.cssText = `
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        `;
        
        section.innerHTML = `
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 2px solid rgba(255, 255, 255, 0.1);">
                <span style="font-size: 2rem;">${icon}</span>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 1.5rem; color: var(--gold); margin: 0; flex: 1;">
                    ${categoryName}
                </h3>
                <span style="background: rgba(212, 175, 55, 0.2); padding: 0.5rem 1rem; border-radius: 50px; color: var(--gold); font-weight: 600; font-size: 0.9rem;">
                    ${validItems.length} items
                </span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem;">
                ${validItems.map((item, index) => {
                    const itemId = `${category}-${index}`;
                    const isChecked = shoppingCheckedItems.has(itemId);
                    return `
                        <div class="shopping-item" style="
                            background: rgba(255, 255, 255, 0.02);
                            border-left: 4px solid var(--gold);
                            border-radius: 8px;
                            padding: 1rem;
                            display: flex;
                            align-items: center;
                            gap: 1rem;
                            transition: all 0.3s ease;
                            cursor: pointer;
                        " onclick="toggleShoppingItem('${itemId}')" onmouseover="this.style.background='rgba(255, 255, 255, 0.05)'" onmouseout="this.style.background='rgba(255, 255, 255, 0.02)'">
                            <div class="shopping-checkbox" id="check-${itemId}" style="
                                width: 24px;
                                height: 24px;
                                min-width: 24px;
                                border: 2px solid var(--gold);
                                border-radius: 6px;
                                cursor: pointer;
                                transition: all 0.3s ease;
                                ${isChecked ? 'background: var(--gold);' : ''}
                            ">
                                ${isChecked ? '<span style="position: absolute; color: var(--black); font-weight: bold;">✓</span>' : ''}
                            </div>
                            <div style="flex: 1;">
                                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.25rem; color: var(--white);">
                                    ${item.nombre}
                                </div>
                                ${item.notas ? `<div style="font-size: 0.85rem; color: var(--silver); font-style: italic;">${item.notas}</div>` : ''}
                            </div>
                            <div style="font-weight: 700; font-size: 1.1rem; color: var(--gold); min-width: 100px; text-align: right; white-space: nowrap;">
                                ${item.cantidad || item.quantity || item.amount || '-'}
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
        
        display.appendChild(section);
    });
    
    if (display.innerHTML === '') {
        display.innerHTML = `
            <div class="empty-state">
                <h3>No hay lista de compra disponible</h3>
                <p style="margin-top: 1rem; color: var(--silver);">
                    Este menú no incluye una lista de compra. Genera un nuevo menú para obtener una lista de compra completa.
                </p>
            </div>
        `;
    }
}

// Toggle shopping item checkbox
function toggleShoppingItem(itemId) {
    const checkbox = document.getElementById(`check-${itemId}`);
    
    if (shoppingCheckedItems.has(itemId)) {
        shoppingCheckedItems.delete(itemId);
        checkbox.style.background = '';
        checkbox.innerHTML = '';
    } else {
        shoppingCheckedItems.add(itemId);
        checkbox.style.background = 'var(--gold)';
        checkbox.innerHTML = '<span style="position: absolute; color: var(--black); font-weight: bold;">✓</span>';
    }
    
    updateShoppingProgress();
}

// Update shopping progress
function updateShoppingProgress() {
    const checked = shoppingCheckedItems.size;
    const total = shoppingTotalItems;
    const percentage = total > 0 ? (checked / total) * 100 : 0;
    
    document.getElementById('progress-text').textContent = `${checked} / ${total} items`;
    document.getElementById('progress-fill').style.width = `${percentage}%`;
}

// Mark all items as purchased
function markAllAsPurchased() {
    // Get all shopping items from the display
    const allCheckboxes = document.querySelectorAll('.shopping-checkbox');
    
    allCheckboxes.forEach(checkbox => {
        const itemId = checkbox.id.replace('check-', '');
        shoppingCheckedItems.add(itemId);
        checkbox.style.background = 'var(--gold)';
        checkbox.innerHTML = '<span style="position: absolute; color: var(--black); font-weight: bold;">✓</span>';
    });
    
    updateShoppingProgress();
    showAlert('All items marked as purchased', 'success');
}

// Clear checked items
function clearCheckedItems() {
    shoppingCheckedItems.clear();
    document.querySelectorAll('.shopping-checkbox').forEach(cb => {
        cb.style.background = '';
        cb.innerHTML = '';
    });
    updateShoppingProgress();
    showAlert('All checks cleared', 'success');
}

// Export to Google format
async function exportToGoogle() {
    // Try to get menu data from current shopping list display
    if (!currentShoppingMenuData) {
        // Try to get data from the displayed shopping list
        const display = document.getElementById('shopping-list-display');
        if (!display || !display.innerHTML.includes('shopping-categories-week')) {
            showAlert('Por favor, carga primero una lista de compra', 'error');
            return;
        }
        
        // Try to reconstruct menu data from displayed content
        showAlert('Por favor, carga primero una lista de compra usando el botón "Cargar Listas"', 'error');
        return;
    }
    
    const menuData = currentShoppingMenuData.menu_data;
    
    if (!menuData) {
        showAlert('No hay datos de menú disponibles', 'error');
        return;
    }
    const adultList = menuData.menu_adultos?.lista_compras?.por_categoria || {};
    const childrenList = menuData.menu_ninos?.lista_compras?.por_categoria || {};
    
    const mergedCategories = mergeShoppingLists(menuData);
    
    // Generate Google-compatible format
    let googleText = `🛒 SHOPPING LIST - Week of ${menuData.semana || 'N/A'}\n`;
    googleText += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
    
    // Add summary
    const adultSummary = menuData.menu_adultos?.lista_compras?.resumen_cantidades || {};
    if (adultSummary.total_items) {
        googleText += `📊 SUMMARY:\n`;
        googleText += `• Total Items: ${adultSummary.total_items}\n`;
        googleText += `• Weight: ${adultSummary.peso_aproximado || 'N/A'}\n`;
        googleText += `• Budget: ${adultSummary.presupuesto_estimado || 'N/A'}\n\n`;
    }
    
    // Add each category
    const categoryOrder = ['frutas_verduras', 'carnes_pescados', 'lacteos_huevos', 'cereales_legumbres', 'despensa', 'congelados', 'otros'];
    const orderedCategories = categoryOrder.filter(cat => mergedCategories[cat] && mergedCategories[cat].length > 0);
    const otherCategories = Object.keys(mergedCategories).filter(cat => !categoryOrder.includes(cat) && mergedCategories[cat] && mergedCategories[cat].length > 0);
    
    [...orderedCategories, ...otherCategories].forEach((category) => {
        const items = mergedCategories[category];
        if (!items || items.length === 0) return;
        
        const categoryName = shoppingCategoryNames[category] || category;
        const icon = shoppingCategoryIcons[category] || '📦';
        
        googleText += `${icon} ${categoryName.toUpperCase()} (${items.length})\n`;
        googleText += `${'─'.repeat(40)}\n`;
        
        items.forEach(item => {
            const itemName = item.nombre || item.name || String(item);
            const itemQuantity = item.cantidad || item.quantity || '';
            const itemNotes = item.notas || item.notes || '';
            
            googleText += `☐ ${itemName}`;
            if (itemQuantity) {
                googleText += ` - ${itemQuantity}`;
            }
            if (itemNotes) {
                googleText += ` (${itemNotes})`;
            }
            googleText += `\n`;
        });
        
        googleText += `\n`;
    });
    
    googleText += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
    googleText += `Generated: ${new Date().toLocaleDateString('es-ES')}\n`;
    
    // Copy to clipboard
    try {
        await navigator.clipboard.writeText(googleText);
        if (typeof showNotification === 'function') {
            showNotification('✅ List copied! Now paste it in Google Keep or Google Docs');
        } else {
            showAlert('✅ List copied! Now paste it in Google Keep or Google Docs', 'success');
        }
        
        // Also download as .txt file
        downloadTextFile(googleText, `shopping-list-${menuData.semana || currentShoppingWeek || 'week'}.txt`);
    } catch (err) {
        console.error('Failed to copy:', err);
        // Fallback: just download
        downloadTextFile(googleText, `shopping-list-${menuData.semana || currentShoppingWeek || 'week'}.txt`);
        if (typeof showNotification === 'function') {
            showNotification('📥 File downloaded! Upload to Google Drive');
        } else {
            showAlert('📥 File downloaded! Upload to Google Drive', 'success');
        }
    }
}

// Download text file
function downloadTextFile(text, filename) {
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Generate simple PDF-friendly text format for printing
function generateSimpleShoppingListText() {
    if (!currentShoppingMenuData) {
        showAlert('Por favor, carga primero una lista de compra', 'error');
        return;
    }
    
    const menuData = currentShoppingMenuData.menu_data;
    if (!menuData) {
        showAlert('No hay datos de menú disponibles', 'error');
        return;
    }
    
    const mergedCategories = mergeShoppingLists(menuData);
    const weekDate = menuData.semana || currentShoppingWeek || 'N/A';
    
    // Generate simple text format
    let text = `SHOPPING LIST\n`;
    text += `Week: ${weekDate}\n`;
    text += `${'='.repeat(50)}\n\n`;
    
    // Add each category
    const categoryOrder = ['frutas_verduras', 'carnes_pescados', 'lacteos_huevos', 'cereales_legumbres', 'despensa', 'congelados', 'otros'];
    const orderedCategories = categoryOrder.filter(cat => mergedCategories[cat] && mergedCategories[cat].length > 0);
    const otherCategories = Object.keys(mergedCategories).filter(cat => !categoryOrder.includes(cat) && mergedCategories[cat] && mergedCategories[cat].length > 0);
    
    [...orderedCategories, ...otherCategories].forEach((category) => {
        const items = mergedCategories[category];
        if (!items || items.length === 0) return;
        
        const categoryName = shoppingCategoryNames[category] || category;
        const icon = shoppingCategoryIcons[category] || '•';
        
        text += `${icon} ${categoryName.toUpperCase()}\n`;
        text += `${'-'.repeat(50)}\n`;
        
        items.forEach(item => {
            const itemName = item.nombre || item.name || String(item);
            const itemQuantity = item.cantidad || item.quantity || '';
            const itemNotes = item.notas || item.notes || '';
            
            text += `  ☐ ${itemName}`;
            if (itemQuantity) {
                text += ` - ${itemQuantity}`;
            }
            if (itemNotes) {
                text += ` (${itemNotes})`;
            }
            text += `\n`;
        });
        
        text += `\n`;
    });
    
    text += `${'='.repeat(50)}\n`;
    text += `Generated: ${new Date().toLocaleDateString('es-ES')}\n`;
    
    // Create a simple HTML page for printing
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Shopping List - ${weekDate}</title>
            <style>
                @page {
                    margin: 1cm;
                    size: A4;
                }
                body {
                    font-family: Arial, sans-serif;
                    font-size: 11pt;
                    line-height: 1.4;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    font-size: 18pt;
                    margin: 0 0 0.5cm 0;
                    padding: 0;
                }
                h2 {
                    font-size: 13pt;
                    margin: 0.4cm 0 0.2cm 0;
                    padding: 0;
                    border-bottom: 1px solid #000;
                }
                .item {
                    margin: 0.1cm 0;
                    padding: 0;
                }
                .category {
                    margin-top: 0.3cm;
                }
            </style>
        </head>
        <body>
            <h1>🛒 Shopping List</h1>
            <p><strong>Week:</strong> ${weekDate}</p>
            <hr>
    `);
    
    [...orderedCategories, ...otherCategories].forEach((category) => {
        const items = mergedCategories[category];
        if (!items || items.length === 0) return;
        
        const categoryName = shoppingCategoryNames[category] || category;
        const icon = shoppingCategoryIcons[category] || '•';
        
        printWindow.document.write(`<div class="category"><h2>${icon} ${categoryName}</h2>`);
        
        items.forEach(item => {
            const itemName = item.nombre || item.name || String(item);
            const itemQuantity = item.cantidad || item.quantity || '';
            const itemNotes = item.notas || item.notes || '';
            
            let itemText = `☐ ${itemName}`;
            if (itemQuantity) {
                itemText += ` - ${itemQuantity}`;
            }
            if (itemNotes) {
                itemText += ` <em>(${itemNotes})</em>`;
            }
            
            printWindow.document.write(`<div class="item">${itemText}</div>`);
        });
        
        printWindow.document.write(`</div>`);
    });
    
    printWindow.document.write(`
            <hr>
            <p style="font-size: 9pt; color: #666;">Generated: ${new Date().toLocaleDateString('es-ES')}</p>
        </body>
        </html>
    `);
    printWindow.document.close();
    
    // Wait for content to load, then print
    setTimeout(() => {
        printWindow.print();
    }, 250);
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, var(--gold), var(--gold-dark));
        color: var(--black);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        font-weight: 600;
        box-shadow: 0 10px 40px rgba(212, 175, 55, 0.4);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Switch tab helper
function switchTab(tabName) {
    console.log(`[SwitchTab] Attempting to switch to ${tabName} tab`);
    
    // Remove active class from all sidebar items
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Add active class to clicked item
    const clickedItem = document.querySelector(`[data-tab="${tabName}"]`);
    if (clickedItem) {
        clickedItem.classList.add('active');
        console.log(`[SwitchTab] Added active class to sidebar item for ${tabName}`);
    } else {
        console.error(`[SwitchTab] Could not find sidebar item with data-tab="${tabName}"`);
        return;
    }
    
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
        console.log(`[SwitchTab] Hidden tab content: ${content.id}`);
    });
    
    // Show selected tab content
    const targetTab = document.getElementById(`${tabName}-tab`);
    if (targetTab) {
        targetTab.classList.add('active');
        console.log(`[SwitchTab] Showing tab content: ${targetTab.id}`);
        
        // Load content for specific tabs
        if (tabName === 'recipes') {
            console.log('[SwitchTab] Loading recipes...');
            // Recipes content is already in HTML, no additional loading needed
        } else if (tabName === 'shopping') {
            console.log('[SwitchTab] Loading shopping list...');
            loadShoppingLists(); // Load shopping list when tab is opened
        }
    } else {
        console.error(`[SwitchTab] Could not find tab content with id="${tabName}-tab"`);
    }
    
    console.log(`[SwitchTab] Successfully switched to ${tabName} tab`);
}

// Menu data storage (kept for potential future use, but no longer used for display)
function storeMenuData(menuData) {
    window.currentMenuData = menuData;
}

// Removed unused functions: renderMenuPreview, openMenuVisualizer, downloadMenuJSON
// Menu is now displayed directly using displayMenu() function

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('[Init] Page loaded, loading family profiles...');
    try {
        loadFamilyProfiles();
        console.log('[Init] Family profiles loading initiated');
        
        // Since menu tab is active by default, load current week menu
        setTimeout(() => {
            console.log('[Init] Loading current week menu (menu tab is active by default)');
            loadCurrentWeekMenu();
        }, 1000); // Small delay to ensure family profiles are loaded first
    } catch (error) {
        console.error('[Init] Error loading family profiles:', error);
    }
});
