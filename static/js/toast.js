// static/js/toast.js
function showToast(title, message, type = 'info', duration = 3000) {
    const container = document.getElementById("toast-container");
    if (!container) return;

    // 1. Create the new toast element
    const toast = document.createElement('div');
    
    // Determine styles and icon based on type
    let bg, border, iconEmoji, progressGradient;
    switch (type) {
        case 'success':
            bg = 'bg-green-100/70 border-green-400';
            iconEmoji = '✅';
            progressGradient = 'linear-gradient(to right, #4ade80, #22c55e)';
            break;
        case 'error':
            bg = 'bg-red-100/70 border-red-400';
            iconEmoji = '❌';
            progressGradient = 'linear-gradient(to right, #f87171, #ef4444)';
            break;
        case 'warning':
            bg = 'bg-yellow-100/70 border-yellow-400';
            iconEmoji = '⚠️';
            progressGradient = 'linear-gradient(to right, #facc15, #eab308)';
            break;
        default: // info
            bg = 'bg-blue-100/70 border-blue-400';
            iconEmoji = 'ℹ️';
            progressGradient = 'linear-gradient(to right, #60a5fa, #3b82f6)';
    }

    // 2. Set the base classes and structure using your original HTML
    toast.className = `w-full max-w-full px-5 py-4 rounded-xl shadow-2xl backdrop-blur-md border-2 ${bg} text-gray-900 opacity-0 -translate-y-10 transition-all duration-300`;
    toast.innerHTML = `
        <div class="flex justify-between items-start gap-3">
            <div class="flex items-center gap-3">
                <span class="text-2xl">${iconEmoji}</span>
                <div>
                    <h3 class="font-semibold text-lg leading-tight">${title}</h3>
                    <p class="text-sm text-gray-700 leading-snug">${message}</p>
                </div>
            </div>
            <button class="toast-close-btn text-gray-500 hover:text-gray-700 text-lg font-bold">&times;</button>
        </div>
        <div class="toast-progress-bar h-1 mt-3 rounded-full scale-x-0 origin-left transition-transform" style="background: ${progressGradient}; transition-duration: ${duration}ms;"></div>
    `;

    // 3. Add it to the container
    container.appendChild(toast);

    // 4. Animate it in
    // We use a tiny timeout to ensure the initial (invisible) state is rendered before the transition starts
    setTimeout(() => {
        toast.classList.remove('opacity-0', '-translate-y-10');
        const progressBar = toast.querySelector('.toast-progress-bar');
        if (progressBar) {
            progressBar.classList.add('scale-x-100');
        }
    }, 10);

    // Function to hide and remove the toast
    const hideAndRemoveToast = () => {
        toast.classList.add('opacity-0');
        // Wait for the fade-out animation to finish before removing
        toast.addEventListener('transitionend', () => {
            toast.remove();
        });
    };

    // 5. Set up auto-hide and the close button
    const autoHideTimeout = setTimeout(hideAndRemoveToast, duration);
    
    const closeButton = toast.querySelector('.toast-close-btn');
    closeButton.onclick = () => {
        clearTimeout(autoHideTimeout); // Stop the auto-hide if closed manually
        hideAndRemoveToast();
    };
}