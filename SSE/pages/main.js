let source;
const button = document.getElementById('start-btn');
const container = document.getElementById('output');
const promptInput = document.getElementById('prompt-input');

function resetForm(){
    promptInput.value = "";
    container.textContent = "";
}
function handleOpen(){
    console.log("Connection opened");
}
function handleMessage(e){
    if (e.data === '[DONE]') {
        source.close();
        button.disabled = false;
        return;
    }
    container.textContent += e.data;
}
function handleError(e){
    console.error("Error occurred:", e);
    source.close();
}

button.addEventListener('click', function(){
    const message = promptInput.value;
    const url = 'http://localhost:8000/generate/text/stream?prompt=' + encodeURIComponent(message);
    source = new EventSource(url);
    source.addEventListener('open', handleOpen, false);
    source.addEventListener('message', handleMessage,false);
    source.addEventListener('error', handleError,false);
})