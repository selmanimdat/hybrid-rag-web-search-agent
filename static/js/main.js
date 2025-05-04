const canvas = document.getElementById("audio-circle");
const ctx = canvas.getContext("2d");
const radius = 90;

function drawCircle(level) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.arc(100, 100, radius + level * 40, 0, 2 * Math.PI);
  ctx.strokeStyle = `rgb(${100 + level*155}, ${level*200}, ${255 - level*100})`;
  ctx.lineWidth = 10;
  ctx.stroke();
}

// Ses verisi al
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const context = new AudioContext();
    const source = context.createMediaStreamSource(stream);
    const analyser = context.createAnalyser();
    source.connect(analyser);

    const dataArray = new Uint8Array(analyser.frequencyBinCount);

    function animate() {
      analyser.getByteFrequencyData(dataArray);
      const avg = dataArray.reduce((a, b) => a + b, 0) / dataArray.length;
      const level = Math.min(avg / 100, 1);
      drawCircle(level);
      requestAnimationFrame(animate);
    }
    animate();
  })
  .catch(err => console.error("Mikrofon erişimi reddedildi:", err));

// Durumu düzenli olarak güncelle
setInterval(() => {
  fetch("/status")
    .then(res => res.json())
    .then(data => {
      document.getElementById("status").innerText = "Durum: " + data.status;
    });
}, 1000);
