<template>
  <div class="mockup-container">
    <!-- Header -->
    <div class="mockup-header">
      <h1>Sistema ASR de Gestión de Inventario</h1>
      <p>Mockups de Pantallas Completos</p>
    </div>

    <!-- Navigation -->
    <div class="mockup-nav">
      <button 
        v-for="screen in screens" 
        :key="screen.id"
        class="nav-btn" 
        :class="{ active: activeScreen === screen.id }"
        @click="setActiveScreen(screen.id)"
      >
        {{ screen.label }}
      </button>
    </div>

    <!-- Dashboard Screen -->
    <div v-show="activeScreen === 'dashboard'" class="screen">
      <div class="dashboard">
        <div class="dashboard-header">
          <h2>Panel de Control</h2>
          <div>Bienvenido de vuelta, {{ currentUser.role }}</div>
        </div>

        <div class="dashboard-stats">
          <div v-for="stat in dashboardStats" :key="stat.label" class="stat-card">
            <div class="stat-value">{{ stat.value }}</div>
            <div>{{ stat.label }}</div>
          </div>
        </div>

        <div class="dashboard-content">
          <div>
            <h3>Análisis de Ventas vs Stock</h3>
            <div class="chart-container">
              <div class="chart-placeholder">
                <div>📊 Gráfico Interactivo de Ventas y Stock</div>
              </div>
            </div>
          </div>
          
          <div class="alerts-panel">
            <h3>🚨 Alertas Activas</h3>
            <div 
              v-for="alert in alerts" 
              :key="alert.id" 
              class="alert-item" 
              :class="alert.type"
            >
              <strong>{{ alert.title }}</strong><br>
              {{ alert.message }}<br>
              <small>{{ alert.detail }}</small>
            </div>
          </div>
        </div>

        <div class="calendar-widget">
          <h3>📅 Calendario Comercial</h3>
          <div class="calendar-grid">
            <div 
              v-for="event in commercialEvents" 
              :key="event.date"
              class="calendar-event"
            >
              <strong>{{ event.date }}</strong><br>{{ event.name }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Inventory Screen -->
    <div v-show="activeScreen === 'inventory'" class="screen">
      <div class="inventory-header">
        <h2>Gestión de Inventario</h2>
        <div class="inventory-controls">
          <input 
            v-model="inventorySearch" 
            type="text" 
            class="search-input" 
            placeholder="Buscar productos..."
          >
          <button class="btn-secondary">Filtrar</button>
          <button class="btn-success" @click="showAddProduct">+ Agregar Producto</button>
        </div>
      </div>

      <table class="inventory-table">
        <thead>
          <tr>
            <th>Producto</th>
            <th>Stock Actual</th>
            <th>En Tránsito</th>
            <th>Ventas Proyectadas</th>
            <th>Demanda Estacional</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td>
              <strong>{{ product.name }}</strong><br>
              <small>SKU: {{ product.sku }}</small>
            </td>
            <td>
              <span class="stock-indicator" :class="product.stockLevel"></span>
              <strong :style="{ color: product.stockColor }">{{ product.currentStock }} unidades</strong>
            </td>
            <td>{{ product.inTransit }} unidades</td>
            <td>{{ product.projectedSales }} unidades/semana</td>
            <td>
              <span class="seasonal-tag" :style="product.seasonalStyle">
                {{ product.seasonalCategory }}
              </span>
            </td>
            <td>
              <div class="action-buttons">
                <button class="btn-sm btn-edit" @click="editProduct(product)">Editar</button>
                <button class="btn-sm btn-delete" @click="deleteProduct(product)">Eliminar</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Projections Screen -->
    <div v-show="activeScreen === 'projections'" class="screen">
      <div class="projections-container">
        <h2>📈 Proyecciones de Stock (ASR Predictor)</h2>
        
        <div class="projection-chart">
          <div class="chart-placeholder">
            <h3>📊 Gráfico de Proyección Semanal de Stock</h3>
            <p>Pronóstico de demanda potenciado por IA basado en tendencias estacionales</p>
          </div>
        </div>

        <div class="recommendations">
          <div 
            v-for="recommendation in recommendations" 
            :key="recommendation.id"
            class="recommendation-card" 
            :class="recommendation.type"
          >
            <h3>{{ recommendation.icon }} {{ recommendation.title }}</h3>
            <p><strong>{{ recommendation.action }}</strong></p>
            <p>{{ recommendation.description }}</p>
            <p>{{ recommendation.suggestion }}</p>
          </div>
        </div>

        <div class="ai-insights">
          <h3>🤖 Insights de IA</h3>
          <ul>
            <li v-for="insight in aiInsights" :key="insight">{{ insight }}</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Reports Screen -->
    <div v-show="activeScreen === 'reports'" class="screen">
      <div class="reports-container">
        <h2>📊 Reportes y Análisis</h2>

        <div class="kpi-grid">
          <div v-for="kpi in kpis" :key="kpi.title" class="kpi-card">
            <h3>{{ kpi.title }}</h3>
            <div class="kpi-value">{{ kpi.value }}</div>
            <p>{{ kpi.description }}</p>
          </div>
        </div>

        <div class="charts-section">
          <h3>📈 Gráficos de Rendimiento</h3>
          <div class="charts-grid">
            <div class="chart-container">
              <div>📊 Ventas vs Stock vs Compras</div>
            </div>
            <div class="chart-container">
              <div>📈 Tendencias de Demanda Estacional</div>
            </div>
          </div>
        </div>

        <div class="download-section">
          <h3>📥 Descargar Reporte</h3>
          <button class="btn-primary" @click="downloadReport">📄 Reporte PDF</button>
        </div>
      </div>
    </div>

    <!-- Users Screen -->
    <div v-show="activeScreen === 'users'" class="screen">
      <div class="users-container">
        <div class="users-header">
          <h2>👥 Gestión de Usuarios</h2>
          <button class="btn-success" @click="showAddUser">+ Agregar Nuevo Usuario</button>
        </div>

        <div v-for="user in users" :key="user.id" class="user-card">
          <div class="user-info">
            <div class="user-avatar">{{ user.initials }}</div>
            <div>
              <h4>{{ user.name }}</h4>
              <p>{{ user.email }}</p>
              <span class="user-role" :class="user.roleClass">{{ user.role }}</span>
            </div>
          </div>
          <div class="user-actions">
            <button class="btn-sm btn-edit" @click="editUser(user)">Editar Permisos</button>
            <button class="btn-sm btn-secondary" @click="viewActivity(user)">Ver Actividad</button>
          </div>
        </div>

        <div v-if="pendingApprovals.length > 0" class="pending-approvals">
          <h4>🔔 Aprobaciones Pendientes</h4>
          <div v-for="approval in pendingApprovals" :key="approval.id" class="approval-item">
            <p><strong>{{ approval.type }}:</strong> {{ approval.description }}</p>
            <div class="approval-actions">
              <button class="btn-success btn-sm" @click="approveRequest(approval)">Aprobar</button>
              <button class="btn-danger btn-sm" @click="rejectRequest(approval)">Rechazar</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Settings Screen -->
    <div v-show="activeScreen === 'settings'" class="screen">
      <div class="settings-container">
        <h2>⚙️ Configuración</h2>

        <div class="settings-section">
          <h3>📅 Fechas Especiales Personalizadas</h3>
          <p>Agrega fechas importantes específicas de tu empresa para una mejor planificación del inventario</p>
          
          <div class="add-date-form">
            <input v-model="newEvent.name" type="text" placeholder="Nombre del evento" class="flex-input">
            <input v-model="newEvent.date" type="date" class="date-input">
            <input v-model="newEvent.impact" type="number" placeholder="Impacto esperado %" class="impact-input">
            <button class="btn-success" @click="addCustomEvent">Agregar Fecha</button>
          </div>

          <div class="custom-dates">
            <div v-for="event in customEvents" :key="event.id" class="date-card">
              <h4>{{ event.icon }} {{ event.name }}</h4>
              <p><strong>Fecha:</strong> {{ event.date }}</p>
              <p><strong>Impacto Esperado:</strong> +{{ event.impact }}% ventas</p>
              <p><strong>Categoría:</strong> {{ event.category }}</p>
              <div class="date-actions">
                <button class="btn-sm btn-edit" @click="editEvent(event)">Editar</button>
                <button class="btn-sm btn-delete" @click="deleteEvent(event)">Eliminar</button>
              </div>
            </div>
          </div>
        </div>

        <div class="settings-section">
          <h3>🎯 Configuración de Predicciones</h3>
          <div class="prediction-settings">
            <div>
              <label>Horizonte de Pronóstico</label>
              <select v-model="predictionSettings.horizon" class="form-select">
                <option value="2weeks">2 semanas</option>
                <option value="1month">1 mes</option>
                <option value="3months">3 meses</option>
                <option value="6months">6 meses</option>
              </select>
            </div>
            <div>
              <label>Nivel de Stock de Seguridad</label>
              <input 
                v-model="predictionSettings.safetyStock" 
                type="number" 
                class="form-input"
              >
              <small>Porcentaje de la demanda promedio para mantener como reserva</small>
            </div>
          </div>
        </div>

        <div class="save-settings">
          <button class="btn-primary" @click="saveSettings">Guardar Configuración</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'InvexMockup',
  setup() {
    const activeScreen = ref('dashboard')
    const inventorySearch = ref('')
    const currentUser = ref({ role: 'Administrador' })
    const predictionSettings = ref({ horizon: '1month', safetyStock: 20 })
    const newEvent = ref({ name: '', date: '', impact: '' })

    const screens = ref([
      { id: 'dashboard', label: 'Dashboard' },
      { id: 'inventory', label: 'Inventario' },
      { id: 'projections', label: 'Proyecciones' },
      { id: 'reports', label: 'Reportes' },
      { id: 'users', label: 'Usuarios' },
      { id: 'settings', label: 'Configuración' }
    ])

    const dashboardStats = ref([
      { label: 'Productos Totales', value: '1,247' },
      { label: 'Ventas Mensuales', value: '$84,350' },
      { label: 'Alertas de Stock Bajo', value: '23' },
      { label: 'Precisión de Inventario', value: '96%' }
    ])

    const alerts = ref([
      { id: 1, type: 'urgent', title: 'Alerta de San Valentín', message: 'Quedan 15 días - Aumento esperado de ventas +30%', detail: 'Revisar inventario de regalos románticos' },
      { id: 2, type: 'warning', title: 'Preparación Halloween', message: '3 semanas hasta Halloween', detail: 'Revisar stock de disfraces y decoraciones' },
      { id: 3, type: '', title: 'Riesgo de Stock', message: '12 productos debajo del umbral mínimo', detail: 'Reabastecimiento inmediato requerido' },
      { id: 4, type: 'success', title: 'Compra Aprobada', message: 'Orden #PO-2024-156 confirmada', detail: 'Entrega esperada en 5 días' }
    ])

    const commercialEvents = ref([
      { date: '14 Feb', name: 'San Valentín' },
      { date: '31 Oct', name: 'Halloween' },
      { date: '29 Nov', name: 'Black Friday' },
      { date: '25 Dic', name: 'Navidad' }
    ])

    const products = ref([
      { id: 1, name: 'Ramo de Rosas Rojas', sku: 'RRB-001', currentStock: 45, inTransit: 200, projectedSales: 350, seasonalCategory: '❤️ San Valentín Alta', stockLevel: 'stock-low', stockColor: '#dc3545', seasonalStyle: { background: '#ffebee', color: '#c62828', padding: '4px 8px', borderRadius: '12px', fontSize: '12px' } },
      { id: 2, name: 'Disfraz Halloween - Bruja', sku: 'HCW-002', currentStock: 150, inTransit: 0, projectedSales: 80, seasonalCategory: '🎃 Halloween', stockLevel: 'stock-medium', stockColor: '#ffc107', seasonalStyle: { background: '#fff3e0', color: '#e65100', padding: '4px 8px', borderRadius: '12px', fontSize: '12px' } },
      { id: 3, name: 'Luces Árbol Navidad', sku: 'CTL-003', currentStock: 850, inTransit: 300, projectedSales: 120, seasonalCategory: '🎄 Temporada Navideña', stockLevel: 'stock-high', stockColor: '#28a745', seasonalStyle: { background: '#e8f5e8', color: '#2e7d32', padding: '4px 8px', borderRadius: '12px', fontSize: '12px' } },
      { id: 4, name: 'Electrónicos Black Friday', sku: 'BFE-004', currentStock: 200, inTransit: 500, projectedSales: 450, seasonalCategory: '⚡ Black Friday', stockLevel: 'stock-medium', stockColor: '#ffc107', seasonalStyle: { background: '#f3e5f5', color: '#6a1b9a', padding: '4px 8px', borderRadius: '12px', fontSize: '12px' } }
    ])

    const recommendations = ref([
      { id: 1, type: 'urgent', icon: '🚨', title: 'Acción Urgente Requerida', action: 'Comprar en 5 días', description: 'El inventario de Ramos de Rosas Rojas se agotará antes de la temporada de San Valentín', suggestion: 'Orden recomendada: 500 unidades' },
      { id: 2, type: 'warning', icon: '⚠️', title: 'Alerta de Riesgo de Stock', action: 'Riesgo de agotarse en 2 semanas', description: 'Los disfraces de Halloween muestran señales de alta demanda', suggestion: 'Orden recomendada: 200 unidades' },
      { id: 3, type: '', icon: '💡', title: 'Oportunidad de Optimización', action: 'Reducir sobrestock', description: 'Las decoraciones navideñas tienen exceso de inventario', suggestion: 'Considerar precios promocionales' }
    ])

    const aiInsights = ref([
      'La demanda de San Valentín es 30% mayor que los datos del año pasado',
      'Las tendencias de disfraces de Halloween muestran que los estilos vintage están ganando popularidad',
      'Se detectaron patrones tempranos de compras navideñas - considerar promociones más tempranas',
      'Se proyecta que la demanda de electrónicos de Black Friday aumente en 45%'
    ])

    const kpis = ref([
      { title: 'Rotación de Inventario', value: '8.5x', description: 'Rotación anual' },
      { title: 'Días de Cobertura', value: '45', description: 'Días de stock' },
      { title: 'Valor de Sobrestock', value: '$12,450', description: 'Inventario excedente' }
    ])

    const users = ref([
      { id: 1, name: 'Juan Pérez', email: 'juan.perez@empresa.com', role: 'Administrador', initials: 'JD', roleClass: 'role-admin' },
      { id: 2, name: 'María Silva', email: 'maria.silva@empresa.com', role: 'Trabajador de Almacén', initials: 'MS', roleClass: 'role-worker' },
      { id: 3, name: 'Roberto García', email: 'roberto.garcia@empresa.com', role: 'Encargado de Inventario', initials: 'RG', roleClass: 'role-worker' }
    ])

    const pendingApprovals = ref([
      { id: 1, type: 'Solicitud de Descuento', description: 'María Silva solicitó aprobación para aplicar 25% descuento en disfraces de Halloween' }
    ])

    const customEvents = ref([
      { id: 1, name: 'Aniversario de la Empresa', date: '15 de Marzo, 2024', impact: 25, category: 'Regalos corporativos, artículos de celebración', icon: '🎂' },
      { id: 2, name: 'Regreso a Clases', date: '20 de Agosto, 2024', impact: 40, category: 'Útiles escolares, mochilas', icon: '🎒' },
      { id: 3, name: 'Temporada de Festivales', date: '1-30 de Junio, 2024', impact: 60, category: 'Equipos de festival, accesorios', icon: '🎵' }
    ])

    const filteredProducts = computed(() => {
      if (!inventorySearch.value) return products.value
      return products.value.filter(product =>
        product.name.toLowerCase().includes(inventorySearch.value.toLowerCase()) ||
        product.sku.toLowerCase().includes(inventorySearch.value.toLowerCase())
      )
    })

    const setActiveScreen = (screenId) => { activeScreen.value = screenId }
    const saveSettings = () => { console.log('Save settings:', predictionSettings.value) }

    const simulateUpdates = () => {
      setInterval(() => {
        const alertElements = document.querySelectorAll('.alert-item')
        if (alertElements.length > 0) {
          const randomAlert = alertElements[Math.floor(Math.random() * alertElements.length)]
          randomAlert.style.transform = 'scale(1.02)'
          setTimeout(() => { randomAlert.style.transform = 'scale(1)' }, 500)
        }
      }, 3000)
    }

    onMounted(() => { simulateUpdates() })

    return {
      activeScreen,
      inventorySearch,
      currentUser,
      predictionSettings,
      newEvent,
      screens,
      dashboardStats,
      alerts,
      commercialEvents,
      products,
      recommendations,
      aiInsights,
      kpis,
      users,
      pendingApprovals,
      customEvents,
      filteredProducts,
      setActiveScreen,
      saveSettings
    }
  }
}
</script>
