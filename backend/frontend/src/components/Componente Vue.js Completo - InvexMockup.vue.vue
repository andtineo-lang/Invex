<!--css-->
<style scoped>
/* Estilos Base */
.mockup-container {
  @apply max-w-6xl mx-auto p-5 min-h-screen;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.mockup-header {
  @apply text-center text-white mb-8;
}

.mockup-header h1 {
  @apply text-3xl font-bold mb-2;
}

/* Navegación */
.mockup-nav {
  @apply rounded-2xl p-5 mb-8 flex justify-center flex-wrap gap-3;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.nav-btn {
  @apply text-white border-0 px-6 py-3 rounded-lg cursor-pointer font-semibold transition-all duration-300;
  background: rgba(255, 255, 255, 0.2);
}

.nav-btn:hover,
.nav-btn.active {
  @apply transform -translate-y-0.5;
  background: rgba(255, 255, 255, 0.3);
}

/* Screens Base */
.screen {
  @apply bg-white rounded-3xl overflow-hidden min-h-screen;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

/* Login Screen */
.login-screen {
  @apply flex min-h-full;
}

.login-left {
  @apply flex-1 p-16 text-white flex flex-col justify-center;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.login-right {
  @apply flex-1 p-16 flex flex-col justify-center;
}

.login-form {
  @apply max-w-md mx-auto w-full;
}

.feature-list {
  @apply mt-8 list-none;
}

.feature-list li {
  @apply mb-3;
}

.form-group {
  @apply mb-5;
}

.form-group label {
  @apply block mb-2 font-semibold text-gray-800;
}

.form-group input,
.form-group select,
.form-select,
.form-input {
  @apply w-full px-4 py-3 border-2 border-gray-200 rounded-lg text-base transition-colors duration-300;
}

.form-group input:focus,
.form-group select:focus,
.form-select:focus,
.form-input:focus {
  @apply outline-none border-blue-400;
}

.form-divider {
  @apply my-8;
}

/* Buttons */
.btn-primary {
  @apply text-white border-0 px-7 py-4 rounded-lg text-base font-semibold cursor-pointer w-full transition-transform duration-300;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.btn-primary:hover {
  @apply transform -translate-y-0.5;
}

.btn-secondary {
  @apply bg-gray-600 text-white border-0 px-5 py-2.5 rounded-lg cursor-pointer;
}

.btn-success {
  @apply bg-green-600 text-white border-0 px-5 py-2.5 rounded-lg cursor-pointer;
}

.btn-sm {
  @apply px-3 py-1.5 border-0 rounded cursor-pointer text-xs;
}

.btn-edit {
  @apply bg-blue-600 text-white;
}

.btn-delete,
.btn-danger {
  @apply bg-red-600 text-white;
}

.register-btn {
  @apply mt-5;
}

/* Subscription Plans */
.subscription-plans {
  @apply flex gap-4 mt-3;
}

.plan {
  @apply flex-1 p-4 border-2 border-gray-200 rounded-lg text-center cursor-pointer transition-all duration-300;
}

.plan:hover,
.plan.selected {
  @apply border-blue-400;
  background: rgba(79, 172, 254, 0.1);
}

.plan h4 {
  @apply font-semibold mb-1;
}

.plan small {
  @apply text-xs text-gray-600;
}

/* Dashboard */
.dashboard {
  @apply p-8;
}

.dashboard-header {
  @apply flex justify-between items-center mb-8 pb-5 border-b-2 border-gray-100;
}

.dashboard-stats {
  @apply grid gap-5 mb-8;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.stat-card {
  @apply text-white p-6 rounded-xl text-center transition-all duration-300;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-value {
  @apply text-4xl font-bold mb-3;
}

.dashboard-content {
  @apply grid gap-8;
  grid-template-columns: 2fr 1fr;
}

.chart-container {
  @apply bg-gray-50 p-6 rounded-xl h-72 flex items-center justify-center border-2 border-dashed border-gray-300;
}

.chart-placeholder {
  @apply text-center;
}

.alerts-panel {
  @apply bg-yellow-50 border border-yellow-200 rounded-xl p-5;
}

.alert-item {
  @apply bg-white p-4 rounded-lg mb-4 border-l-4;
}

.alert-item:last-child {
  @apply mb-0;
}

.alert-item.urgent {
  @apply border-l-red-500;
}

.alert-item.warning {
  @apply border-l-orange-500;
}

.alert-item.success {
  @apply border-l-green-500;
}

.calendar-widget {
  @apply bg-gray-50 p-5 rounded-xl mt-5;
}

.calendar-grid {
  @apply grid grid-cols-4 gap-3 mt-4;
}

.calendar-event {
  @apply p-3 bg-blue-50 rounded text-center text-sm;
}

/* Inventory */
.inventory-header {
  @apply flex justify-between items-center px-8 py-5 border-b-2 border-gray-100;
}

.inventory-controls {
  @apply flex gap-3 items-center;
}

.search-input {
  @apply px-4 py-2.5 border-2 border-gray-200 rounded-lg w-80;
}

.inventory-table {
  @apply w-full border-collapse mx-8 my-5;
}

.inventory-table th,
.inventory-table td {
  @apply px-4 py-4 text-left border-b border-gray-200;
}

.inventory-table th {
  @apply bg-gray-50 font-semibold;
}

.stock-indicator {
  @apply inline-block w-3 h-3 rounded-full mr-2;
}

.stock-high {
  @apply bg-green-500;
}

.stock-medium {
  @apply bg-yellow-500;
}

.stock-low {
  @apply bg-red-500;
}

.action-buttons {
  @apply flex gap-2;
}

.seasonal-tag {
  @apply inline-block;
}

/* Projections */
.projections-container {
  @apply p-8;
}

.projection-chart {
  @apply bg-gray-50 h-96 rounded-xl my-5 flex items-center justify-center border-2 border-dashed border-gray-300;
}

.recommendations {
  @apply grid gap-5 mt-5;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.recommendation-card {
  @apply p-5 rounded-xl text-white;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
}

.recommendation-card.urgent {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
}

.recommendation-card.warning {
  background: linear-gradient(135deg, #ffa726 0%, #ffcc02 100%);
}

.ai-insights {
  @apply bg-gray-50 p-5 rounded-xl mt-5;
}

.ai-insights ul {
  @apply mt-4;
}

.ai-insights li {
  @apply mb-2;
}

/* Reports */
.reports-container {
  @apply p-8;
}

.kpi-grid {
  @apply grid gap-5 mb-8;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

.kpi-card {
  @apply text-white p-5 rounded-xl text-center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.kpi-value {
  @apply text-2xl my-3 font-bold;
}

.charts-section {
  @apply bg-gray-50 p-6 rounded-xl mb-5;
}

.charts-grid {
  @apply grid grid-cols-2 gap-5 mt-4;
}

.download-section {
  @apply bg-gray-50 p-5 rounded-xl text-center;
}

/* Users */
.users-container {
  @apply p-8;
}

.users-header {
  @apply flex justify-between items-center mb-5;
}

.user-card {
  @apply bg-white border border-gray-200 rounded-lg p-5 mb-4 flex justify-between items-center transition-all duration-300;
}

.user-info {
  @apply flex items-center gap-4;
}

.user-avatar {
  @apply w-12 h-12 rounded-full flex items-center justify-center text-white font-bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.user-role {
  @apply px-3 py-1 rounded-full text-xs font-semibold;
}

.role-admin {
  @apply bg-blue-50 text-blue-700;
}

.role-worker {
  @apply bg-purple-50 text-purple-700;
}

.user-actions {
  @apply flex gap-2;
}

.pending-approvals {
  @apply bg-yellow-50 border border-yellow-200 rounded-lg p-4 mt-5;
}

.approval-item {
  @apply mt-3;
}

.approval-actions {
  @apply mt-2;
}

/* Settings */
.settings-container {
  @apply p-8;
}

.settings-section {
  @apply bg-white border border-gray-200 rounded-lg p-5 mb-5;
}

.add-date-form {
  @apply flex gap-4 my-4 flex-wrap;
}

.flex-input {
  @apply flex-1 min-w-48 px-3 py-2 border border-gray-300 rounded;
}

.date-input {
  @apply px-3 py-2 border border-gray-300 rounded;
}

.impact-input {
  @apply w-40 px-3 py-2 border border-gray-300 rounded;
}

.custom-dates {
  @apply grid gap-4 mt-4;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.date-card {
  @apply bg-gray-50 p-4 rounded-lg border border-gray-200 transition-all duration-300;
}

.date-actions {
  @apply mt-3;
}

.prediction-settings {
  @apply grid gap-4 mt-4;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.save-settings {
  @apply text-center mt-8;
}

/* Responsive */
@media (max-width: 768px) {
  .login-screen {
    @apply flex-col;
  }
  
  .dashboard-content {
    @apply grid-cols-1;
  }
  
  .subscription-plans {
    @apply flex-col;
  }
  
  .mockup-nav {
    @apply p-4;
  }
  
  .nav-btn {
    @apply text-sm px-4 py-2;
  }

  .charts-grid {
    @apply grid-cols-1;
  }

  .add-date-form {
    @apply flex-col;
  }

  .flex-input,
  .date-input,
  .impact-input {
    @apply w-full;
  }

  .calendar-grid {
    @apply grid-cols-2;
  }
}

</style>





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

    <!-- Login Screen -->
    <div v-show="activeScreen === 'login'" class="screen active">
      <div class="login-screen">
        <div class="login-left">
          <h2>Gestor de Inventario ASR</h2>
          <p>Gestión inteligente de inventario con predicciones potenciadas por IA</p>
          <ul class="feature-list">
            <li>✓ Seguimiento de stock en tiempo real</li>
            <li>✓ Predicciones de demanda estacional</li>
            <li>✓ Recomendaciones automáticas de compra</li>
            <li>✓ Alertas y notificaciones personalizadas</li>
          </ul>
        </div>
        <div class="login-right">
          <div class="login-form">
            <!-- Login Form -->
            <h3>Iniciar Sesión</h3>
            <form @submit.prevent="handleLogin">
              <div class="form-group">
                <label>Correo Electrónico</label>
                <input v-model="loginForm.email" type="email" placeholder="Ingresa tu correo">
              </div>
              <div class="form-group">
                <label>Contraseña</label>
                <input v-model="loginForm.password" type="password" placeholder="Ingresa tu contraseña">
              </div>
              <button type="submit" class="btn-primary">Iniciar Sesión</button>
            </form>
            
            <hr class="form-divider">
            
            <!-- Registration Form -->
            <h4>Crear Nueva Cuenta</h4>
            <form @submit.prevent="handleRegister">
              <div class="form-group">
                <label>Nombre de la Empresa</label>
                <input v-model="registerForm.companyName" type="text" placeholder="Nombre de tu empresa">
              </div>
              <div class="form-group">
                <label>Correo Electrónico</label>
                <input v-model="registerForm.email" type="email" placeholder="empresa@email.com">
              </div>
              <div class="form-group">
                <label>Contraseña</label>
                <input v-model="registerForm.password" type="password" placeholder="Crear contraseña">
              </div>
              
              <label>Plan de Suscripción</label>
              <div class="subscription-plans">
                <div 
                  v-for="plan in subscriptionPlans" 
                  :key="plan.id"
                  class="plan" 
                  :class="{ selected: registerForm.selectedPlan === plan.id }"
                  @click="registerForm.selectedPlan = plan.id"
                >
                  <h4>{{ plan.name }}</h4>
                  <p>${{ plan.price }}/mes</p>
                  <small v-if="plan.discount">{{ plan.discount }}</small>
                </div>
              </div>
              
              <button type="submit" class="btn-primary register-btn">Iniciar Prueba Gratuita</button>
            </form>
          </div>
        </div>
      </div>
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
