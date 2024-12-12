import {autoResizeQueryField} from "./ui.js";
let filter_id = 0

export let filter_instances = new Array();

export class FiltersManager {
    constructor(graph){
        this.graph = graph;
        this.container = main;
        this.id = filter_id;
        filter_id += 1;
        filter_instances.push(this);
    }

    build(){
        let G = this.graph

        let holder = document.createElement("div");
        holder.classList.add("card", "overflow-hidden", "p-0", "m-1", "col-5");
        holder.style = "resize: both;";
        holder.innerHTML = `
<div class="card-header d-flex p-1">
    <span>
        <h5>Filters</h5>
    </span> 
    <span class="header-buttons ms-auto d-flex"> 
        <button class="filter-close btn-close my-auto" aria-label="Close"></button>
    </span>
</div>

<div class="vizbody">
</div>

<div class="vizfooter mt-3"></div>
</div>
    `;
        this.holder = holder;
        let that = this;
        holder.querySelector('.filter-close').addEventListener("click", function(){
            G.delete_onready_callback(that.draw_callback);
            filter_instances.splice(filter_instances.indexOf(this), 1);
            holder.remove(); 
        });        

        this.container.prepend(holder);

        let filters_holder = document.createElement("div");
        filters_holder.classList.add("p-2", "overflow-y-auto");
        

        let content_holder = holder.querySelector(".vizbody");
        content_holder.appendChild(filters_holder);
        this.content_holder = content_holder;
        this.build_filters_table(content_holder, this.graph);
       
    }

    async refresh_table() {
        this.build_filters_table();
    }

    async build_filters_table() {
        // Clear the container before adding buttons
        this.content_holder.innerHTML = "";
    
        // Get the list of filters from the API
        let filters_list = await this.graph.api.get.list_filters(this.graph.gname);
    
        // If no filters exist, display a message
        if (filters_list.length === 0) {
            let no_filter_message = document.createElement("p");
            no_filter_message.innerHTML = "This graph contains no filter";
            this.content_holder.appendChild(no_filter_message);
            return;  // Exit the function if no filters are present
        }
    
        let G = this.graph;
        // Create a table element to hold the filters
        let table = document.createElement("table");
        table.classList.add("table", "table-striped");
    
        // Create the table header
        let thead = document.createElement("thead");
        let headerRow = document.createElement("tr");
    
        let headerName = document.createElement("th");
        headerName.innerHTML = "Filter Name";
        headerRow.appendChild(headerName);
    
        let headerDescription = document.createElement("th");
        headerDescription.innerHTML = "Description";
        headerRow.appendChild(headerDescription);
    
        thead.appendChild(headerRow);
        table.appendChild(thead);
    
        // Create the table body and populate it with the filters
        let tbody = document.createElement("tbody");
    
        filters_list.forEach(filter => {
            let row = document.createElement("tr");
            row.classList.add("overflow-y:scroll");
    
            // Create a cell for the filter name
            let nameCell = document.createElement("td");
            nameCell.innerHTML = filter[0];
            row.appendChild(nameCell);
    
            // Create a cell for the filter description
            let descriptionCell = document.createElement("td");
            descriptionCell.innerHTML = filter[1] || "No description available";

            descriptionCell.addEventListener("click", function() {
                queryField.value +=filter[1];
                autoResizeQueryField();
            });

            row.appendChild(descriptionCell);

            let destroyCell = document.createElement("td");
            let destroyButton = document.createElement("button");
            destroyButton.classList.add("btn", "btn-outline-danger");
            destroyButton.innerHTML="X";
            destroyButton.addEventListener("click", function() {
                G.api.post.remove_filter(G.gname, filter[0]);
                row.remove();
            })
            destroyCell.appendChild(destroyButton);
            row.appendChild(destroyCell);
    
            // Append the row to the table body
            tbody.appendChild(row);
        });
    
        // Append the body to the table
        table.appendChild(tbody);
    
        // Append the table to the container
        this.content_holder.appendChild(table);
    }
}
