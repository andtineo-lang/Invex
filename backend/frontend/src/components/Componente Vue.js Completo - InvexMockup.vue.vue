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
