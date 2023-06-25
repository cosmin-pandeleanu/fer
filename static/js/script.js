/**
 *  Incarcarea fisierelor locale
 **/

// Funcție pentru a procesa fișierul
function processFile() {
    // Obțineți elementul <input> pentru fișier
    const fileInput = document.getElementById('file-input');
    // Obțineți primul fișier selectat
    const file = fileInput.files[0];

    // Verificați dacă a fost selectat un fișier
    if (file) {
        // Creați un obiect FormData pentru a trimite fișierul către server
        const formData = new FormData();
        formData.append('uploaded-file', file);

        // Trimiteți cererea către metoda din Flask și primiți rezultatul
        $.ajax({
            url: '/process_file',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            error: function (error) {
                console.log(error);
            }
        });
        // Adaugă un delay de 3 secunde
        setTimeout(function () {
            // Refresh pagina
            location.reload();
        }, 3000);
    } else {
        console.log('Nu a fost selectat niciun fișier.');
        alert('Nu a fost selectat niciun fișier.');
    }
}

/**
 *  Web Camera
 **/


// Accesarea elementelor HTML
var videoContainer = document.getElementById('video-container');
var videoElement;
var isCameraStarted = false;
var photoWasTaken = false;

// Funcție pentru a porni camera web și afișarea previzualizării camerei web
function startCamera() {
    if (isCameraStarted) {
        console.log('Camera web este deja pornită!');
        alert('Camera web este deja pornită!');
        return;
    }
    navigator.mediaDevices.getUserMedia({video: true, audio: false})
        .then(function (stream) {
            // Crearea elementului video și configurarea surselor media
            videoElement = document.createElement('video');
            videoElement.id = 'video-element';
            videoElement.srcObject = stream;
            videoElement.play();

            // Adăugarea elementului video în container
            videoContainer.appendChild(videoElement);

            // Actualizarea variabilei pentru a indica că camera a fost pornită
            isCameraStarted = true;
        })
        .catch(function (error) {
            console.log('Eroare la accesarea camerei web:', error);
        });
}

// Funcție pentru a face o fotografie
function capturePhoto() {
    if (!isCameraStarted) {
        console.log('Camera web nu este pornită.');
        alert('Camera web nu este pornită!');
        return;
    }

    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // Salvarea imaginii în format base64
    const imageData = canvas.toDataURL('image/png');

    // Creați un obiect FormData pentru a trimite imaginea către server
    const formData = new FormData();
    formData.append('image_data', imageData);

    // Trimiteți cererea către ruta de server Flask pentru a salva imaginea
    $.ajax({
        url: '/save_photo',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log('Imagine salvată cu succes:', response);
        },
        error: function (error) {
            console.log('Eroare la salvarea imaginii:', error);
        }
    });

    photoWasTaken = true;
}

// Funcție pentru a opri camera web și eliminarea previzualizării
function stopCamera() {
    if (!isCameraStarted) {
        console.log('Camera web nu este pornită!');
        alert('Camera web nu este pornită!');
        return;
    }
    isCameraStarted = false;

    // Opriți sursa media și eliberați resursele
    const stream = videoElement.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(function (track) {
        track.stop();
    });

    // Eliminarea elementului video din container
    videoContainer.removeChild(videoElement);
    videoElement = null;

}

// Funcție pentru a procesa fișierul și a actualiza src-ul imaginii
function processFileWebCamera() {
    // Trimiteți cererea către metoda din Flask și primiți rezultatul
    if (photoWasTaken) {
        $.ajax({
            url: '/process_file_webcamera',
            type: 'POST',
            contentType: false,
            processData: false,
            error: function (error) {
                console.log(error);
            }
        });
        // Adaugă un delay de 3 secunde
        setTimeout(function () {
            // Refresh pagina
            location.reload();
        }, 3000);
    }
    else {
        console.log('Nu s-a realizat poza!');
        alert('Nu s-a realizat poza!');
    }
}
