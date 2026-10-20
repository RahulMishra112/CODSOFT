document.addEventListener('DOMContentLoaded', () => {
    const webcamVideo = document.getElementById('webcam-video');
    const startStreamBtn = document.getElementById('start-stream-btn');
    const stopStreamBtn = document.getElementById('stop-stream-btn');
    const outputImage = document.getElementById('output-image');
    const faceCount = document.getElementById('face-count');
    const streamStatus = document.getElementById('stream-status');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const enrollName = document.getElementById('enroll-name');
    const enrollBtn = document.getElementById('enroll-btn');

    let streamActive = false;
    let currentFrameBase64 = null;
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');

    // 1. Start Real-Time Webcam Stream
    startStreamBtn.addEventListener('click', async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: { ideal: 640 }, height: { ideal: 480 } } 
            });
            webcamVideo.srcObject = stream;
            webcamVideo.classList.remove('hidden');
            startStreamBtn.classList.add('hidden');
            stopStreamBtn.classList.remove('hidden');
            
            streamActive = true;
            streamStatus.textContent = "Live Streaming";
            streamStatus.style.color = "#00f2fe";

            // Begin continuous real-time loop
            requestAnimationFrame(processStreamFrame);
        } catch (err) {
            alert("Unable to access webcam. Check browser permissions.");
        }
    });

    // 2. Stop Real-Time Webcam Stream
    stopStreamBtn.addEventListener('click', () => {
        streamActive = false;
        if (webcamVideo.srcObject) {
            webcamVideo.srcObject.getTracks().forEach(track => track.stop());
        }
        webcamVideo.classList.add('hidden');
        startStreamBtn.classList.remove('hidden');
        stopStreamBtn.classList.add('hidden');
        streamStatus.textContent = "Stream Stopped";
        streamStatus.style.color = "#94a3b8";
    });

    // 3. Real-Time Continuous Frame Capture and Transmission
    async function processStreamFrame() {
        if (!streamActive) return;

        if (webcamVideo.videoWidth > 0 && webcamVideo.videoHeight > 0) {
            canvas.width = webcamVideo.videoWidth;
            canvas.height = webcamVideo.videoHeight;
            ctx.drawImage(webcamVideo, 0, 0, canvas.width, canvas.height);
            currentFrameBase64 = canvas.toDataURL('image/jpeg', 0.7);

            try {
                const response = await fetch('/api/detect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: currentFrameBase64 })
                });

                const data = await response.json();
                if (data.processed_image && streamActive) {
                    outputImage.src = data.processed_image;
                    outputImage.classList.remove('hidden');
                    faceCount.textContent = `${data.count} Face(s) Detected`;
                }
            } catch (e) {
                console.error("Frame processing error:", e);
            }
        }

        // Trigger next frame processing interval (~15-20 FPS)
        if (streamActive) {
            setTimeout(() => {
                requestAnimationFrame(processStreamFrame);
            }, 50);
        }
    }

    // 4. Fallback File Upload Analysis
    dropZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const reader = new FileReader();
            reader.onload = (evt) => {
                currentFrameBase64 = evt.target.result;
                sendSingleImage(currentFrameBase64);
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    });

    async function sendSingleImage(base64Str) {
        const response = await fetch('/api/detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: base64Str })
        });
        const data = await response.json();
        if (data.processed_image) {
            outputImage.src = data.processed_image;
            outputImage.classList.remove('hidden');
            faceCount.textContent = `${data.count} Face(s) Detected`;
        }
    }

    // 5. Participant Enrollment
    enrollBtn.addEventListener('click', async () => {
        const name = enrollName.value.trim();
        if (!name || !currentFrameBase64) {
            return alert("Please enter a name and start the stream or upload an image first.");
        }

        const response = await fetch('/api/enroll', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name, image: currentFrameBase64 })
        });

        const data = await response.json();
        if (data.error) alert(data.error);
        else {
            alert(data.message);
            enrollName.value = '';
        }
    });
});