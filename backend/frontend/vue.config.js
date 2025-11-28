// vue.config.js (ACTUALIZADO)

const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  
  // ==============================================
  // CONFIGURACIÓN DE PROXY PARA DJANGO REST FRAMEWORK
  // ==============================================
  devServer: {
    // Escucha en el puerto predeterminado de Vue (8080)
    port: 8080, 
    
    // Configuración del proxy
    proxy: {
      // Regla: Captura cualquier llamada que empiece con '/api' 
      '^/api': {
        // Redirige la llamada a la dirección de tu servidor Django
        target: 'http://localhost:8000', 
        
        // Cambia el encabezado 'Host' al destino (necesario para la comunicación entre servidores)
        changeOrigin: true, 
        
        // El proxy NO elimina el prefijo '/api' (porque tus URLs de Django lo usan)
        pathRewrite: { '^/api': '/api' }, 
        
        // Asegúrate de que no haya problemas de certificado en desarrollo
        secure: false, 
      },
    }
  }
})