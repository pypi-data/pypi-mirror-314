import { BaseViz } from "../visualisation.js";
import { modal } from "../ui.js";
import { PARTIALLY } from "../config.js";
import { AlignerViz } from "../aligner.js";

function format_metadata(metadatas){
    return metadatas.map((metadata) => `${metadata.type}(${metadata.id})`).join(", ");
}

export class TableViz extends BaseViz{

    constructor(graph, container){
        super(graph, container);
        this.aligner;
    }

    get_container(container) {
        return container;
    }
    
    get vizname(){
        return "Table";
    }

    build() {
        super.build();
        let that = this;
        let button_handler = document.querySelector("#button_span_" + this.viz_id);
        let add_aligner_button = document.createElement("button");
        add_aligner_button.classList.add("btn", "my-auto", "mx-2");
        add_aligner_button.innerHTML = "Open aligner";
        button_handler.prepend(add_aligner_button);
        add_aligner_button.addEventListener("click", function () {
            that.setUpAligner();
        });
    }

    setUpAligner() {
        let that = this;
        try {
            that.aligner.remove();
        }
        catch {
            ;
        };
        let aligner = (new AlignerViz(this)).build();
        this.aligner = aligner;
    }

    prepare(){
        let that = this;
        this.body.innerHTML = `
<table class="viztable table table-striped w-100">
    <thead>
        <tr>
            <th style="width:6em">id</th>
            <th>Sequence</th>
            <th>metadata</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>`;
        this.tbody = this.body.querySelector("tbody");
        this.table = this.body.querySelector("table");
        this.table.style.tableLayout = "fixed";

    }

    _draw() {
        super._draw();
        if (this.aligner != undefined) {
            this.aligner.setUpListeners();
        }
    }

    draw_node(node){
            let tr = document.createElement("tr");
            let data = this.graph.node_data(node);
            if (data == PARTIALLY)
                return undefined;
        
            let td = document.createElement("td");
            tr.innerHTML = `
<td>${node}</td>
<td><div class="long_cell">${data.seq}</div></td>
<td><div class="long_cell">${format_metadata(data.metadatas)}</div></td>
`;
            return tr;
    }

    attach_node(node){
        this.tbody.appendChild(node);
    }

    returnRows() {
        let rows = this.tbody.querySelectorAll("tr");
        return rows;
    }
}

