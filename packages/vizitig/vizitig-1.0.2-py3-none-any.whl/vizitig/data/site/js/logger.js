let log_holder = document.createElement("div");
document.body.prepend(log_holder);
log_holder.classList.add("w-100", "position-fixed", "top-0","z-3");

export class Logger {
    log(msg){
        console.log("log", msg);
    }

    error(msg){
        let error = document.createElement("div");
        error.classList.add("alert", "alert-danger","w-50", "alert-dismissible", "mx-auto", "z-3", "my-3");
        error.innerHTML = `${msg}
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`;
        log_holder.appendChild(error);
    }

    warn(msg){
        console.log("warn", msg)
    }
}
