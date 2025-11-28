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

    <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-end sm:items-center justify-center z-50">
      <div class="bg-white rounded-t-2xl sm:rounded-xl p-5 sm:p-6 w-full max-w-md sm:max-w-lg shadow-xl">
        <h3 class="text-lg font-semibold mb-4">Agregar Nuevo Producto</h3>
        <form @submit.prevent="addProduct">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Producto</label>
              <input v-model="newProduct.name" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">SKU</label>
              <input v-model="newProduct.sku" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500">
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Stock Inicial</label>
                <input v-model.number="newProduct.stock" type="number" min="0" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Ventas Proy./sem</label>
                <input v-model.number="newProduct.projectedSales" type="number" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500">
              </div>
            </div>
          </div>
          <div class="flex flex-col sm:flex-row sm:justify-end gap-3 mt-6">
            <button type="button" @click="showAddModal = false" class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
              Cancelar
            </button>
            <button type="submit" class="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700">
              Agregar
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showEditModal" class="fixed inset-0 bg-black/50 flex items-end sm:items-center justify-center z-50">
      <div class="bg-white rounded-t-2xl sm:rounded-xl p-5 sm:p-6 w-full max-w-md sm:max-w-lg shadow-xl">
        <h3 class="text-lg font-semibold mb-4">Editar Producto</h3>
        <form @submit.prevent="updateProduct">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Producto</label>
              <input v-model="editingProduct.name" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">SKU</label>
              <input v-model="editingProduct.sku" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500">
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Stock Actual</label>
                <input v-model.number="editingProduct.stock" type="number" min="0" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Ventas Proy./sem</label>
                <input v-model.number="editingProduct.projectedSales" type="number" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500">
              </div>
            </div>
          </div>
          <div class="flex flex-col sm:flex-row sm:justify-end gap-3 mt-6">
            <button type="button" @click="showEditModal = false" class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
              Cancelar
            </button>
            <button type="submit" class="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700">
              Guardar Cambios
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axiosInstance from '@/api/axios.js';

// --- ESTADO DEL COMPONENTE ---
const products = ref([])
const searchTerm = ref('')
const isLoading = ref(true)
const errorMessage = ref(null)
const showAddModal = ref(false)
const newProduct = ref({ name: '', sku: '', stock: 0, projectedSales: 0 })
const showEditModal = ref(false)
const editingProduct = ref(null)

// --- LÓGICA DE LA API ---
async function fetchProducts() {
  isLoading.value = true
  errorMessage.value = null
  try {
    const response = await axiosInstance.get('/productos/')
    products.value = response.data.map(p => ({
      id: p.id,
      name: p.nombre,
      sku: p.sku,
      stock: p.stock,
      inTransit: p.inTransit,
      projectedSales: p.projectedSales,
      seasonal: p.seasonal,
      proyeccion_status: p.proyeccion_status,
      proyeccion_cantidad: p.proyeccion_cantidad
    }));
  } catch (error) {
    console.error("Error al obtener productos:", error)
    errorMessage.value = "No se pudieron cargar los productos. Por favor, intenta recargar la página."
  } finally {
    isLoading.value = false
  }
}

async function addProduct() {
  const payload = {
    nombre: newProduct.value.name,
    sku: newProduct.value.sku,
    stock_data: {
      stock_actual: newProduct.value.stock,
      ventas_proyectadas: newProduct.value.projectedSales,
      stock_transito: 0,
      demanda_estacional: "Normal"
    }
  }
  try {
    await axiosInstance.post('/productos/', payload)
    await fetchProducts()
    showAddModal.value = false
    newProduct.value = { name: '', sku: '', stock: 0, projectedSales: 0 }
  } catch (error) {
    console.error("Error al agregar producto:", error.response ? error.response.data : error)
    alert("Hubo un error al guardar el producto.")
  }
}

async function deleteProduct(productId) {
  if (!confirm('¿Estás seguro de que quieres eliminar este producto?')) return
  try {
    await axiosInstance.delete(`/productos/${productId}/`)
    await fetchProducts()
  } catch (error) {
    console.error("Error al eliminar producto:", error)
    alert("Hubo un error al eliminar el producto.")
  }
}

function openEdit(product) {
  editingProduct.value = { ...product }
  showEditModal.value = true
}

async function updateProduct() {
  if (!editingProduct.value) return
  const payload = {
    nombre: editingProduct.value.name,
    sku: editingProduct.value.sku,
    stock_data: {
      stock_actual: editingProduct.value.stock,
      ventas_proyectadas: editingProduct.value.projectedSales,
    }
  }
  try {
    await axiosInstance.patch(`/productos/${editingProduct.value.id}/`, payload)
    await fetchProducts()
    showEditModal.value = false
  } catch (error) {
    console.error("Error al actualizar el producto:", error.response ? error.response.data : error)
    alert("Hubo un error al actualizar el producto.")
  }
}

// --- LÓGICA DEL COMPONENTE ---
onMounted(() => {
  fetchProducts()
})

const filteredProducts = computed(() => {
  if (!searchTerm.value) return products.value
  const q = searchTerm.value.toLowerCase()
  return products.value.filter(p => p.name.toLowerCase().includes(q) || (p.sku && p.sku.toLowerCase().includes(q)))
})

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

const getProyeccionClass = (status) => {
  if (status === 'Comprar Ahora') return 'text-red-600'
  if (status === 'Revisar Pronto') return 'text-yellow-600'
  return 'text-green-600'
}
</script>