window.addEventListener('load', () => {
  if (!('serviceWorker' in navigator)) {
    // service workers not supported 😣
    return
  }

  navigator.serviceWorker.register('/service_worker', {scope: '/'}).then(
    () => {
     console.log("Service Worker Registered Successfully 👍")
    },
    err => {
      console.error('SW registration failed! 😱', err)
    }
  )
})
