import { BaseViz } from "./visualisation.js";
import {autoResizeQueryField} from "./ui.js";
let debounceTimer;
let meta_id=0;
export class MetaViz extends BaseViz{

    constructor(graph){
        super();
        this.graph = graph;
        this.container = main;
        this.id = meta_id;
        meta_id += 1;
    }
    

    build(){
        let G = this.graph
        queryField.addEventListener("input", function() {
            autoResizeQueryField();
        });

        let holder = document.createElement("div");
        holder.classList.add("col-5", "card", "overflow-hidden", "p-0", "m-1");
        holder.style = "height: 45vh; resize: both;";
        holder.innerHTML = `
<div class="vizhead card-header  p-1">
    <div class="p-0 vizmenu_main">
        <div class="container-fluid d-flex "> 
        <span>
           <h5>Metadata</h5>
        </span> 
         <span class="header-buttons ms-auto d-flex"> 
             <button class="viz-close btn-close my-auto" aria-label="Close"></button>
         </span>
    </div>
    <div class="vizbody">
        <input type="text" id="metadata_field_${this.id}" class="form-control" placeholder="Filter metadata here">
        <div class="form-floating">
            <select name="metadata" id="metadata_selector_${this.id}" class="form-select metadata_selector">
                <option value="">--Please choose a metadata type to explore--</option>
            </select>
            <label for="metadata_selector" class="form-label">Select a metadata type:</label>
        </div>
    </div>
    <div class="vizfooter mt-3"></div>
</div>
    `;
        this.holder = holder;
        let that = this;
        holder.querySelector('.viz-close').addEventListener("click", function(){
            G.delete_onready_callback(that.draw_callback);
            holder.remove(); 
        });
        // closing the viz
        //holder.querySelector('button[class="btn-close"]').addEventListener("click", function(){
            // that.graph.delete_onready_callback(that.draw_callback);
            // holder.remove(); 
        //    holder.remove();
        //});
        

        this.container.prepend(holder);

        let buttons_holder = document.createElement("div");
        buttons_holder.classList.add("p-2", "overflow-y-auto");
        holder.appendChild(buttons_holder);

        G.metadata_types_list.forEach(function(type){
            const option = document.createElement('option');
            const metadataList = G.metadata_vars_values[type];
            option.value = type;
            option.innerHTML = type;
            
            option.addEventListener("click", function() {
                buttons_holder.innerHTML = "";
                build_metadata_buttons(buttons_holder, metadataList)
            
            });
            document.querySelector(".metadata_selector").appendChild(option);
        });

        document.getElementById(`metadata_field_${this.id}`).addEventListener('input', function() {
            clearTimeout(debounceTimer);

            const filterText = this.value; // Get the current value of the textarea
            // Rebuild the buttons with the filter applied
            let type = document.querySelector(".metadata_selector").value;
            const metadataList = G.metadata_vars_values[type];
            debounceTimer = setTimeout(function() {
                // Rebuild the buttons with the filter applied
                build_metadata_buttons(buttons_holder, metadataList, filterText);
            }, 200); // 1000 milliseconds = 1 second
        });
    }
}


// function build_metadata_buttons(container, metadataList) {
//     for (const [key, element ] of Object.entries(metadataList)) {
//         let button = document.createElement("button");
//         button.classList.add("btn", "btn-primary");
//         button.innerHTML = key;
//         button.addEventListener("click", function(){
//             queryField.value += element.type + '(' + key + ') ';
//             autoResizeQueryField();
//         })
//         container.appendChild(button);
//     }
// }

function build_metadata_buttons(container, metadataList, filterText = "") {
    // Clear the container before adding buttons
    container.innerHTML = "";

    // Loop through the metadataList and create buttons for keys that match the filterText
    for (const [key, element] of Object.entries(metadataList)) {
        // Check if the key includes the filter text (case-insensitive)
        if (key.toLowerCase().includes(filterText.toLowerCase())) {
            let button = document.createElement("button");
            button.classList.add("btn", "btn-outline-primary", "btn-sm", "m-1");
            button.innerHTML = key;
            button.addEventListener("click", function() {
                queryField.value += element.type + `(${key})`;
                autoResizeQueryField();
            });
            container.appendChild(button);
        }
    }
}
