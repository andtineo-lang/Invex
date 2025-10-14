<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between mb-6">
      <h2 class="text-2xl sm:text-3xl font-bold text-gray-900">Gestión de Inventario</h2>
      <div class="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4 w-full sm:w-auto">
        <div class="relative w-full sm:w-72">
          <input v-model="searchTerm" type="text" placeholder="Buscar productos..." class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm sm:text-base">
          <svg class="pointer-events-none absolute left-3 top-2.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
        <button @click="showAddModal = true" class="inline-flex justify-center items-center bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded-lg font-medium transition-colors text-sm sm:text-base">
          + Agregar Producto
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-10 text-gray-500">Cargando productos...</div>
    <div v-if="errorMessage" class="text-center py-10 text-red-600">{{ errorMessage }}</div>

    <div v-if="!isLoading && !errorMessage">
      <div class="grid grid-cols-1 gap-3 sm:hidden">
        <article v-for="product in filteredProducts" :key="product.id" class="bg-white rounded-lg shadow p-4">
          <div class="flex items-start justify-between">
            <div>
              <h3 class="font-semibold text-gray-900 leading-tight">{{ product.name }}</h3>
              <p class="text-xs text-gray-500">SKU: {{ product.sku }}</p>
            </div>
            <span :class="getSeasonalClass(product.seasonal)" class="px-2 py-0.5 text-[10px] font-medium rounded-full whitespace-nowrap">
              {{ product.seasonal }}
            </span>
          </div>
          <dl class="mt-3 grid grid-cols-2 gap-3 text-sm">
            <div>
              <dt class="text-gray-500">Stock</dt>
              <dd>
                <span :class="getStockClass(product.stock)" class="px-2 py-0.5 text-xs font-semibold rounded-full">
                  {{ product.stock }}
                </span>
              </dd>
            </div>
            <div>
              <dt class="text-gray-500">En tránsito</dt>
              <dd class="font-medium text-gray-900">{{ product.inTransit }}</dd>
            </div>
            <div>
              <dt class="text-gray-500">Ventas proj.</dt>
              <dd class="font-medium text-gray-900">{{ product.projectedSales }}/sem</dd>
            </div>
            <div>
              <dt class="text-gray-500">Proyección</dt>
              <dd class="font-semibold" :class="getProyeccionClass(product.proyeccion_status)">
                <span v-if="product.proyeccion_status === 'Comprar Ahora'">
                  Comprar {{ product.proyeccion_cantidad }}
                </span>
                <span v-else>
                  {{ product.proyeccion_status }}
                </span>
              </dd>
            </div>
          </dl>
          <div class="mt-3 flex justify-end gap-4 text-sm font-medium">
            <button class="text-blue-600 hover:text-blue-800" @click="openEdit(product)">Editar</button>
            <button @click="deleteProduct(product.id)" class="text-red-600 hover:text-red-800">Eliminar</button>
          </div>
        </article>
      </div>

      <div class="hidden sm:block bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Producto</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock Actual</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">En Tránsito</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ventas Proyectadas</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Proyección de Compra</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Demanda Estacional</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="product in filteredProducts" :key="product.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ product.name }}</div>
                    <div class="text-sm text-gray-500">SKU: {{ product.sku }}</div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStockClass(product.stock)" class="px-2 py-1 text-xs font-semibold rounded-full">
                    {{ product.stock }} unidades
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ product.inTransit }} unidades</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ product.projectedSales }} unidades/semana</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold" :class="getProyeccionClass(product.proyeccion_status)">
                  <div v-if="product.proyeccion_status === 'Comprar Ahora'">
                    Comprar {{ product.proyeccion_cantidad }} unidades
                  </div>
                  <div v-else>
                    {{ product.proyeccion_status }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getSeasonalClass(product.seasonal)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ product.seasonal }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button class="text-blue-600 hover:text-blue-900" @click="openEdit(product)">Editar</button>
                  <button @click="deleteProduct(product.id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="showAddModal" class="fixed inset-0 bg-black/50 ...">
      </div>
    <div v-if="showEditModal" class="fixed inset-0 bg-black/50 ...">
      </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/productos/'

// --- ESTADO DEL COMPONENTE (sin cambios) ---
const products = ref([])
const searchTerm = ref('')
const isLoading = ref(true)
const errorMessage = ref(null)
const showAddModal = ref(false)
const newProduct = ref({ name: '', sku: '', stock: 0, projectedSales: 0 })
const showEditModal = ref(false)
const editingProduct = ref(null)

// --- LÓGICA DE LA API (actualizada para recibir los nuevos datos) ---
async function fetchProducts() {
  isLoading.value = true
  errorMessage.value = null
  try {
    const response = await axios.get(API_URL)
    products.value = response.data.map(p => ({
      id: p.id,
      name: p.nombre,
      sku: p.sku,
      stock: p.stock,
      inTransit: p.inTransit,
      projectedSales: p.projectedSales,
      seasonal: p.seasonal,
      proyeccion_status: p.proyeccion_status,       // <-- Dato nuevo
      proyeccion_cantidad: p.proyeccion_cantidad  // <-- Dato nuevo
    }));
  } catch (error) {
    console.error("Error al obtener productos:", error)
    errorMessage.value = "No se pudieron cargar los productos. Asegúrate de haber iniciado sesión."
  } finally {
    isLoading.value = false
  }
}

// --- RESTO DE LAS FUNCIONES DE LA API (sin cambios) ---
async function addProduct() { /* ... */ }
async function deleteProduct(productId) { /* ... */ }
function openEdit(product) { /* ... */ }
async function updateProduct() { /* ... */ }


// --- LÓGICA DEL COMPONENTE ---
onMounted(() => {
  fetchProducts()
})

const filteredProducts = computed(() => {
  if (!searchTerm.value) return products.value
  const q = searchTerm.value.toLowerCase()
  return products.value.filter(p => p.name.toLowerCase().includes(q) || (p.sku && p.sku.toLowerCase().includes(q)))
})

// --- FUNCIONES DE ESTILO (con la nueva función de proyección) ---
const getStockClass = (stock) => {
  if (stock < 100) return 'bg-red-100 text-red-800'
  if (stock < 300) return 'bg-yellow-100 text-yellow-800'
  return 'bg-green-100 text-green-800'
}

const getSeasonalClass = (seasonal) => {
  const classes = {
    'San Valentín Alta': 'bg-pink-100 text-pink-800',
    'Pico Halloween': 'bg-orange-100 text-orange-800',
    'Temporada Navideña': 'bg-green-100 text-green-800',
    'Pico Black Friday': 'bg-purple-100 text-purple-800'
  }
  return classes[seasonal] || 'bg-gray-100 text-gray-800'
}

// NUEVA FUNCIÓN para dar color al estado de la proyección
const getProyeccionClass = (status) => {
  if (status === 'Comprar Ahora') return 'text-red-600'
  if (status === 'Revisar Pronto') return 'text-yellow-600'
  return 'text-green-600'
}
</script>