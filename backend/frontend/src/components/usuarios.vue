<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <!-- Encabezado -->
    <div class="mb-6">
      <div class="flex items-center space-x-2 mb-2">
        <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M17 20h5v-2a3 3 0 00-3-3h-2M6 20H1v-2a3 3 0 013-3h2m7-6h.01M12 12a9 9 0 110-18 9 9 0 010 18z" />
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Gestión de Usuarios</h2>
      </div>
    </div>

    <!-- Botón Agregar Nuevo Usuario -->
    <div class="flex justify-end mb-6">
      <button @click="agregarUsuario"
        class="bg-green-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-green-600 transition">
        + Agregar Nuevo Usuario
      </button>
    </div>

    <!-- Lista de Usuarios -->
    <div class="bg-white rounded-lg shadow-lg divide-y">
      <div v-for="usuario in usuarios" :key="usuario.id" class="flex items-center justify-between p-4">
        <div class="flex items-center space-x-4">
          <!-- Avatar con iniciales -->
          <div class="w-12 h-12 flex items-center justify-center rounded-full bg-purple-500 text-white font-bold">
            {{ usuario.iniciales }}
          </div>
          <div>
            <h4 class="text-lg font-bold text-gray-900">{{ usuario.nombre }}</h4>
            <p class="text-sm text-gray-600">{{ usuario.correo }}</p>
            <span :class="getRolClass(usuario.rol)"
              class="inline-block mt-1 px-2 py-1 text-xs font-semibold rounded-full">
              {{ usuario.rol }}
            </span>
          </div>
        </div>
        <div class="flex space-x-2">
          <button @click="editarPermisos(usuario)"
            class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition">
            Editar Permisos
          </button>
          <button @click="verActividad(usuario)"
            class="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600 transition">
            Ver Actividad
          </button>
        </div>
      </div>
    </div>

    <!-- Aprobaciones Pendientes -->
    <div class="mt-8 bg-yellow-100 border-l-4 border-yellow-500 rounded-lg p-4">
      <h3 class="text-lg font-bold text-yellow-700 flex items-center space-x-2 mb-2">
        <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M12 18h.01M9 21h6a2 2 0 002-2v-4a2 2 0 00-2-2h-6a2 2 0 00-2 2v4a2 2 0 002 2z" />
        </svg>
        <span>Aprobaciones Pendientes</span>
      </h3>
      <ul class="list-disc list-inside text-gray-700 space-y-1">
        <li v-for="(aprobacion, index) in aprobacionesPendientes" :key="index">
          {{ aprobacion }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Lista de usuarios
const usuarios = ref([
  {
    id: 1,
    iniciales: 'JP',
    nombre: 'Juan Pérez',
    correo: 'juan.perez@empresa.com',
    rol: 'Administrador'
  },
  {
    id: 2,
    iniciales: 'MS',
    nombre: 'María Silva',
    correo: 'maria.silva@empresa.com',
    rol: 'Trabajador de Almacén'
  },
  {
    id: 3,
    iniciales: 'RG',
    nombre: 'Roberto García',
    correo: 'roberto.garcia@empresa.com',
    rol: 'Encargado de Inventario'
  }
])

// Aprobaciones pendientes
const aprobacionesPendientes = ref([
  'Solicitud de Descuento: María Silva solicitó un 25% de descuento en disfraces de Halloween.',
  'Cambio de Stock: Roberto García propuso ajustar el inventario de luces navideñas.',
  'Permiso de acceso: Se requiere aprobación para un nuevo usuario.'
])

const agregarUsuario = () => {
  alert('Funcionalidad para agregar nuevo usuario')
}

const editarPermisos = (usuario) => {
  alert(`Editando permisos para: ${usuario.nombre}`)
}

const verActividad = (usuario) => {
  alert(`Mostrando actividad de: ${usuario.nombre}`)
}

const getRolClass = (rol) => {
  const roles = {
    'Administrador': 'bg-blue-100 text-blue-800',
    'Trabajador de Almacén': 'bg-purple-100 text-purple-800',
    'Encargado de Inventario': 'bg-green-100 text-green-800'
  }
  return roles[rol] || 'bg-gray-100 text-gray-800'
}
</script>
