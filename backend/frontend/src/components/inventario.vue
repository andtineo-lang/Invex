<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <!-- Header con búsqueda y botón agregar -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold text-gray-900">Gestión de Inventario</h2>
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Buscar productos..."
            class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          >
          <svg class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
        <button
          @click="showModal = true"
          class="bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
        >
          + Agregar Producto
        </button>
      </div>
    </div>

    <!-- Tabla de inventario -->
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Producto</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock Actual</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">En Tránsito</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ventas Proyectadas</th>
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
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ product.inTransit }} unidades
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ product.projectedSales }} unidades/semana
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getSeasonalClass(product.seasonal)" class="px-2 py-1 text-xs font-medium rounded-full">
                {{ product.seasonal }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
              <button class="text-blue-600 hover:text-blue-900">Editar</button>
              <button class="text-red-600 hover:text-red-900">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para agregar producto -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
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
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Stock Inicial</label>
              <input v-model.number="newProduct.stock" type="number" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500">
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button type="button" @click="showModal = false" class="px-4 py-2 text-gray-600 hover:text-gray-800">
              Cancelar
            </button>
            <button type="submit" class="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700">
              Agregar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed } from 'vue'
const searchTerm = ref('')
const showModal = ref(false)


const products = ref([
  {
    id: 1,
    name: 'Ramo de Rosas Rojas',
    sku: 'RRB-001',
    stock: 45,
    inTransit: 200,
    projectedSales: 350,
    seasonal: 'San Valentín Alta'
  },
  {
    id: 2,
    name: 'Disfraz Halloween - Bruja',
    sku: 'HCW-002',
    stock: 150,
    inTransit: 0,
    projectedSales: 80,
    seasonal: 'Pico Halloween'
  },
  {
    id: 3,
    name: 'Luces Árbol Navidad',
    sku: 'CTL-003',
    stock: 850,
    inTransit: 300,
    projectedSales: 120,
    seasonal: 'Temporada Navideña'
  },
  {
    id: 4,
    name: 'Electrónicos Black Friday',
    sku: 'BFE-004',
    stock: 200,
    inTransit: 500,
    projectedSales: 450,
    seasonal: 'Pico Black Friday'
  }
])

const newProduct = ref({
  name: '',
  sku: '',
  stock: 0
})

const filteredProducts = computed(() => {
  if (!searchTerm.value) return products.value
  return products.value.filter(product =>
    product.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    product.sku.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
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

const addProduct = () => {
  const product = {
    id: products.value.length + 1,
    name: newProduct.value.name,
    sku: newProduct.value.sku,
    stock: newProduct.value.stock,
    inTransit: 0,
    projectedSales: 0,
    seasonal: 'Normal'
  }
  
  products.value.push(product)
  
  newProduct.value = {
    name: '',
    sku: '',
    stock: 0
  }
  
  showModal.value = false
}
</script>