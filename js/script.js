// Initialize the ozone progress bar. Call initOzoneBar(progress) with a number 0-100.
window.addEventListener('load', function () {
  const bar = document.getElementById('ozone-bar');
  // No template expressions here; supply progress via initOzoneBar or a data attribute.
  const datasetProgress = bar && bar.dataset && bar.dataset.progress;
  const targetWidth = datasetProgress ? parseFloat(datasetProgress) : 0;

  // Small delay so the animation is visible after page paint
  setTimeout(function () {
    if (bar) bar.style.width = Math.max(0, Math.min(100, targetWidth)) + '%';
  }, 300);
});

// Optional helper to set progress from server-rendered templates
function initOzoneBar(progress) {
  const bar = document.getElementById('ozone-bar');
  if (!bar) return;
  const value = typeof progress === 'number' ? progress : parseFloat(progress) || 0;
  bar.style.width = Math.max(0, Math.min(100, value)) + '%';
}