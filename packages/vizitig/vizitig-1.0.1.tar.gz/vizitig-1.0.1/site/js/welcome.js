import {API} from "./api.js";
import {API_HREF} from "./config.js";
import {Logger} from "./logger.js";
import {trash, edit, copy, dl } from "./ico.js";

let api = new API(API_HREF, new Logger());
api.build().then(build);
let index_types = null;

function clean_name(name){
    return name.replace(".", "_")
}

upload_graph_form.onsubmit = async function (event){
    event.preventDefault();
    let formdata = new FormData(this);
    api.post.upload_graph(formdata.get("name"), formdata);
}


async function refresh_log(gname){ // we refresh the log dynamically

    let gname_clean= clean_name(gname);
    let modal_log = document.querySelector(`#open_log_${gname_clean}`);
    let tbody = modal_log.querySelector("tbody");
    let last_log = tbody.children.length;
    let logs = await api.get.get_log(gname);
    if (logs.length == 0){
        bootstrap.Modal.getInstance(modal_log).hide();
        await build();
        return;
    }
        
    logs = logs.splice(last_log)
    for (const log of logs){
        let td = document.createElement("tr");
        tbody.insertBefore(td, tbody.children[0]);
        for (const val of log.split("::")){
            let tr = document.createElement("td");
            tr.innerHTML = val;
            td.appendChild(tr);
        }
    }
    if (modal_log.classList.contains("show")){
        console.log("refresh_log"); 
        setTimeout(()=>refresh_log(gname), 500); // updated every 500ms if the the modal is displayed
    }
}

function build_modal_delete(gname){
    let gname_clean= clean_name(gname);
    let modal_delete = document.createElement("div"); // delete the graph?
    modal_delete.innerHTML = format_modal_delete(gname, gname_clean);
    modal_delete.setAttribute("id", `check_delete_${gname_clean}`);
    modal_delete.setAttribute("tabindex", "-1");
    modal_delete.classList.add("modal", "fade", "check");

    modals.appendChild(modal_delete);
    modal_delete.querySelector(".delete_graph_btn").onclick = async function(){
        await api.delete.delete_graph(gname);
        bootstrap.Modal.getInstance(modal_delete).hide();
        await build();
    }
}


async function build(){
    graphs_list_holder.innerHTML = "";
    modals.innerHTML = "";
    let v = await api.get.version();
    version.innerHTML = v;
    let graphs_list = await api.get.graphs_list();
    index_types = await api.get.index_types();
    for (const [gname, gdict] of Object.entries(graphs_list)){
        let tr = document.createElement("tr");
        let gname_clean= clean_name(gname);
        graphs_list_holder.appendChild(tr);
        build_modal_delete(gname_clean);
        if (gdict.error){
            tr.innerHTML = format_row_broken(gname, gname_clean, gdict);
            continue;
        }
        tr.innerHTML = format_row(gname, gname_clean, gdict);

        tr.querySelector(`#${gname_clean}_copy`).onclick = async function(){
            await api.post.duplicate(gname);
            await build();
        }
        let modal_log = document.createElement("div"); // the log button should be display only if log_exists.
        modal_log.classList.add("modal", "modal-xl");
        modal_log.setAttribute("id", `open_log_${gname_clean}`);
        modal_log.innerHTML = format_modal_log(gname);
        modal_log.style.maxHeight = "90vh";
        modal_log.addEventListener("show.bs.modal", async function(){
            refresh_log(gname);
        });
        modals.appendChild(modal_log);

        if (gdict.log_exists){
            document.getElementById(`log_btn_${gname_clean}`).classList.remove("d-none");
            document.getElementById(`${gname_clean}_detail`).setAttribute("disabled", "");
            document.getElementById(`${gname_clean}_copy`).setAttribute("disabled", "");
        }

        let modal_option = document.createElement("div"); // editing the graph
        modals.appendChild(modal_option);
        modal_option.innerHTML = format_modal_option(gname, gname_clean, gdict)
        modal_option.setAttribute("id", `operation_${gname_clean}`);
        modal_option.setAttribute("tabindex", "-1");
        modal_option.classList.add("modal", "fade", "check", "modal-lg");

        for (const form of modal_option.querySelectorAll("form"))
            form.addEventListener("submit", async function(event){ event.preventDefault() 
                let formData = new FormData(this);
                formData.set("name", gname); 
                let api_endpoint = api.post[this.getAttribute("api")];
                api_endpoint(formData);
                bootstrap.Modal.getInstance(modal_option).hide();
                await build();
                
            });
            modal_option.querySelector(`#rename_${gname_clean}`).addEventListener("submit", async function(){
            await api.post.rename_graph(gname, form.get("name"));
            bootstrap.Modal.getInstance(modal_option).hide();
        });
    }
}
console.log(api);
async function track_log(){ 
    let graphs_list = await api.get.graphs_list();
    for (const [gname, gdict] of Object.entries(graphs_list)){
        let modal_log = document.getElementById(`log_btn_${clean_name(gname)}`);
        if (modal_log == null && gdict.error == undefined){
            await build();
        } else {
            if (gdict.log_exists){
                if (modal_log.classList.contains("d-none")){
                    modal_log.classList.remove("d-none");
                    await build();
                }
            }
            else 
                if (!modal_log.classList.contains("d-none"))
                    await build();
        }
    }
}
setInterval(track_log, 3000)
function format_index(index_list){
    return index_list.map(e=>`${e.type}(${e.size})`).join(", ")
}
function format_row_broken(gname, gname_clean, gdict){
    return `
<td><a href="graph.html?graph=${gname}" class="link-danger link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover" disabled>${gname}</a></td> 
<td> Broken Graph </td>
<td></td>
<td></td>
<td></td>
<td></td>
<td class="text-end">
    <button id="log_btn_${gname_clean}" class="btn btn-sm btn-warning d-none" data-bs-toggle="modal" data-bs-target="#open_log_${gname_clean}" disabled>log</button>
    <div class="btn-group btn-group-sm" role="group" id="btn_group_edit_${gname_clean}">
        <button id="${gname_clean}_detail" class="btn btn-outline-secondary"  data-bs-toggle="modal" data-bs-target="#operation_${gname_clean}" disabled> ${edit} </button>
        <button id="${gname_clean}_copy" class="btn btn-outline-secondary" disabled> ${copy} </button>
        <a href="files/${gname}.db" download type="button" class="btn btn-outline-secondary"> ${dl} </a>
        <button class="btn btn-outline-secondary" value="delete" data-bs-toggle="modal" data-bs-target="#check_delete_${gname_clean}">${trash}</button>
    </div>
</td>`;

}

function format_row(gname, gname_clean, gdict){
    return `
<td><a href="graph.html?graph=${gname}" class="link-dark link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">${gname}</a></td> 
<td> ${gdict.k}</td>
<td>${gdict["node nb"]}</td>
<td>${gdict["edge nb"]}</td>
<td>${gdict.file_size}</td>
<td>${format_index(gdict["index"])}</td>
<td class="text-end">
    <button id="log_btn_${gname_clean}" class="btn btn-sm btn-warning d-none" data-bs-toggle="modal" data-bs-target="#open_log_${gname_clean}">log</button>
    <div class="btn-group btn-group-sm" role="group" id="btn_group_edit_${gname_clean}">
        <button id="${gname_clean}_detail" class="btn btn-outline-secondary"  data-bs-toggle="modal" data-bs-target="#operation_${gname_clean}"> ${edit} </button>
        <button id="${gname_clean}_copy" class="btn btn-outline-secondary"> ${copy} </button>
        <a href="files/${gname}.db" download type="button" class="btn btn-outline-secondary"> ${dl} </a>
        <button class="btn btn-outline-secondary" value="delete" data-bs-toggle="modal" data-bs-target="#check_delete_${gname_clean}">${trash}</button>
    </div>
</td>`;
}

function format_modal_log(gname){
    return `
<div class="modal-dialog container">
    <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">Logs of ${gname}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body container overflow-auto">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Event</th>
                        <th>Timestamp</th>
                        <th>Call level</th>
                        <th>local_time/total_time</th>
                        <th>message</th>
                        <th>caller</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        </div>
    </div>
</div>`;
}

function format_modal_delete(gname){
    return `
<div class="modal-dialog container">
    <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">Are you sure to delete ${gname} ?</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body container">
            <div class="row">
                <div class="col text-end">
                    <button class="btn btn-secondary mx-auto" data-bs-dismiss="modal"> Cancel </button>
                </div>
                <div class="col">
                    <button class="btn btn-danger delete_graph_btn mx-auto"> Delete graph</button>
                </div>
            </div>
        </div>
    </div>
</div>`;
}
function format_index_choices(){
    return index_types.map(function(index_type){
        return `<option value="${index_type}">${index_type}</option>`;
    }).join("\n");
}

function format_index_delete(gname, gdict){
    if (gdict["index"].length == 0) return "";
    let index_butt_list = gdict["index"].map((idx)=>
        `<form class="row p-2 border-bottom" api="drop_index"> 
                <input type="hidden" name="index_type" value="${idx.type}">
                <div class="col-3">
                    ${idx.type}(${idx.size}) 
                </div>
                <div class="col-2 ms-auto my-auto text-end">
                    <button class="btn btn-outline-danger" type="submit" value="delete">${trash}</button>
                </div>
        </form>
        `).join("\n");
    
    return `${index_butt_list}`;
}

function format_modal_option(gname, gname_clean, gdict){
    return`
    <div class="modal-dialog container">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Graph: ${gname}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body container">
                ${format_index_delete(gname, gdict)}
                <form class="row p-2 border-bottom" id="index_${gname_clean}" api="build_index">
                    <div class="col-4">
                        <div class="form-floating">
                            <select name="index_type" id="index_type_choice_${gname_clean}" class="form-select" >
                                <option selected disabled> </option>
                                ${format_index_choices()}
                            </select>
                            <label for="rename_input_${gname_clean}"> Index Type</label>
                        </div>
                    </div>

                    <div class="col-2 ms-auto my-auto text-end">
                        <input type="submit" class="btn btn-sm btn-outline-primary" value="Build">
                    </div>
                </form>
                <form class="row p-2 border-bottom" id="rename_${gname_clean}">
                    <div class="col-4">
                        <div class="form-floating">
                            <input name="name" id="rename_input_${gname_clean}" class="form-control" value="${gname}" required>
                            <label for="rename_input_${gname_clean}"> name </label>
                        </div>
                    </div>

                    <div class="col-2 ms-auto my-auto text-end">
                        <input type="submit" class="btn btn-sm btn-outline-primary" value="Rename">
                    </div>
                </form>
                <!---
                <form class="row p-2 border-bottom" id="tag_${gname_clean}">
                    <div class="col-4">
                        <div class="form-floating">
                            <input  id="rename_input_${gname_clean}" class="form-control" required>
                            <label for="rename_input_${gname_clean}"> Tag name </label>
                        </div>
                    </div>
                    <div class="col-4 my-auto">
                        <input type="file" class="col form-control" name="file", accept="fa" required>
                    </div>

                    <div class="col-2 ms-auto my-auto text-end">
                        <input type="submit" class="btn btn-sm btn-outline-primary" value="Tag">
                    </div>
                </form>
                <form class="row p-2" id="annotate_${gname_clean}">
                    <div class="col-5 my-auto">
                        <label> Reference sequence </label>
                        <input type="file" class="col form-control" name="file", accept="fa" required>
                    </div>
                    <div class="col-5 my-auto">
                        <label> GTF or GFF file </label>
                        <input type="file" class="col form-control" name="file", accept="GTF, GFF" required>
                    </div>

                    <div class="col-2 my-auto ms-auto text-end">
                        <input type="submit" class="btn btn-sm btn-outline-primary" value="Annotate">
                    </div>
                </form>
                !--->
            </div>
        </div>
    </div>
</div>
    `
}
