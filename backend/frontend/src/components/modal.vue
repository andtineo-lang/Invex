<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-2xl shadow-lg p-6 max-w-md w-full text-center">
      <h2 class="text-xl font-bold mb-4">{{ title }}</h2>
      <p class="text-gray-600 mb-6">{{ message }}</p>
      <button 
        @click="$emit('close')" 
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        Cerrar
      </button>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
defineProps({
  show: Boolean,
  title: String,
  message: String
})

defineEmits(['close'])
/* eslint-enable no-undef */
</script>