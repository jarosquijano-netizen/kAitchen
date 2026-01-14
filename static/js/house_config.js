// House Configuration Functions
let houseConfig = {
    num_habitaciones: 3,
    num_banos: 2,
    num_salas: 2,
    num_cocinas: 1,
    superficie_total: 120,
    tipo_piso: 'apartamento',
    tiene_jardin: 'no',
    mascotas: 'no',
    notas_casa: ''
};

// Load house configuration from API
async function loadHouseConfig() {
    try {
        const result = await API.get('/api/house/config');
        if (result.success && result.data) {
            houseConfig = result.data;
            
            // Update form fields
            Object.keys(houseConfig).forEach(key => {
                const element = document.getElementById(key);
                if (element) {
                    // Handle checkboxes differently
                    if (element.type === 'checkbox') {
                        element.checked = houseConfig[key] === true || houseConfig[key] === 1;
                    } else {
                        element.value = houseConfig[key];
                    }
                }
            });
            
            showHouseConfigStatus('Configuración de casa cargada desde base de datos', 'success');
        } else {
            console.log('Using default house configuration');
        }
    } catch (error) {
        console.error('Error loading house config:', error);
    }
}

// Save house configuration
async function saveHouseConfig() {
    try {
        // Get values from form
        const form = document.getElementById('houseConfigForm');
        const formData = new FormData(form);
        
        // Convert to object
        const configData = {};
        for (let [key, value] of formData.entries()) {
            // Handle checkboxes
            const element = document.getElementById(key);
            if (element && element.type === 'checkbox') {
                configData[key] = element.checked;
            } else {
                configData[key] = value;
            }
        }
        
        // Save to API
        const result = await API.post('/api/house/config', configData);
        
        if (result.success) {
            showHouseConfigStatus('✅ Configuración guardada correctamente en la base de datos', 'success');
            // Reload to get updated data
            setTimeout(() => loadHouseConfig(), 500);
        } else {
            showHouseConfigStatus('Error: ' + (result.error || 'Error desconocido'), 'error');
        }
        
    } catch (error) {
        console.error('Error saving house config:', error);
        showHouseConfigStatus('Error al guardar configuración', 'error');
    }
}

// Apply house configuration to cleaning system
function applyHouseConfigToCleaning() {
    console.log('[HouseConfig] Applying configuration to cleaning system:', houseConfig);
    
    // This will be used to optimize cleaning tasks based on house configuration
    // For example: more bathrooms = more bathroom cleaning tasks
    // More surface area = more frequent cleaning
    // Pets = additional cleaning tasks
}

// Optimize cleaning tasks based on house configuration
async function optimizeCleaningTasks() {
    console.log('[HouseConfig] Optimizing cleaning tasks based on house configuration...');
    
    try {
        const result = await API.post('/api/cleaning/generate-smart-plan', {
            house_config: houseConfig
        });
        
        if (result.success) {
            const optimizations = [];
            
            // Bathroom optimization
            if (houseConfig.num_banos > 1) {
                optimizations.push(`Añadidas tareas para ${houseConfig.num_banos} baños`);
            }
            
            // Surface area optimization
            if (houseConfig.superficie_total > 100) {
                optimizations.push('Frecuencia de limpieza ajustada para superficie grande');
            }
            
            // Pet optimization
            if (houseConfig.mascotas !== 'no') {
                optimizations.push('Añadidas tareas específicas para mascotas');
            }
            
            // Garden/terrace optimization
            if (houseConfig.tiene_jardin !== 'no') {
                optimizations.push('Añadidas tareas de exterior');
            }
            
            showHouseConfigStatus('✅ Optimizaciones aplicadas: ' + optimizations.join(', '), 'success');
            
            // Here you could update the cleaning UI with the new plan
            if (result.data && result.data.plan) {
                console.log('Smart cleaning plan generated:', result.data.plan);
            }
        } else {
            showHouseConfigStatus('Error al generar plan de limpieza', 'error');
        }
    } catch (error) {
        console.error('Error optimizing cleaning tasks:', error);
        showHouseConfigStatus('Error al optimizar tareas', 'error');
    }
}

// Show status messages for house configuration
function showHouseConfigStatus(message, type = 'info') {
    const statusDiv = document.getElementById('house-config-status');
    if (!statusDiv) return;
    
    const alertClass = type === 'success' ? 'success' : type === 'error' ? 'error' : 'info';
    const bgColor = type === 'success' ? 'rgba(72, 187, 120, 0.1)' : 
                   type === 'error' ? 'rgba(245, 101, 101, 0.1)' : 
                   'rgba(59, 130, 246, 0.1)';
    
    statusDiv.innerHTML = `
        <div style="background: ${bgColor}; border: 1px solid ${type === 'success' ? '#48bb78' : type === 'error' ? '#f56565' : '#3b82f6'}; 
                    color: white; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
            ${message}
        </div>
    `;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        statusDiv.innerHTML = '';
    }, 5000);
}

// Initialize house configuration on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener for house configuration form
    const houseForm = document.getElementById('houseConfigForm');
    if (houseForm) {
        houseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveHouseConfig();
        });
    }
    
    // Load saved configuration from API
    loadHouseConfig();
});

// Export functions for global access
window.loadHouseConfig = loadHouseConfig;
window.saveHouseConfig = saveHouseConfig;
window.optimizeCleaningTasks = optimizeCleaningTasks;
