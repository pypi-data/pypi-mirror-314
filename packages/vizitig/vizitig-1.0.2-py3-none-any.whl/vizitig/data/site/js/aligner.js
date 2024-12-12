import { BaseViz } from "./visualisation.js";

export class AlignerViz extends BaseViz{

    constructor(linked_table){
        super();
        this.graph = linked_table.graph;
        this.container = main;
        this.linked_table = linked_table;
        this.id = linked_table.viz_id;
    }
    

    build(){
        let G = this.graph;
        let id = this.id;

        let holder = document.createElement("div");
        holder.classList.add("card", "overflow-hidden", "p-0", "m-1", "col-5");
        holder.style = "resize: both;";
        holder.innerHTML = `
<div class="card-header d-flex p-1">
    <span>
        <h5> Aligner</h5>
    </span> 
    <span class="header-buttons ms-auto d-flex"> 
        <button  id="aligner_close_${this.id}" class="filter-close btn-close my-auto" aria-label="Close"></button>
    </span>
</div>

<div class="vizbody card-body p-0">
    <form class="row border-bottom p-2">
        <div class="col-3">
            <div class="form-floating">
                <input name="node1" id="nodeid1_${id}" type="text" class="form-control" required pattern="\\d+">
                <label class="form-label" for="floatingInputGroup1">NodeId1</label>
            </div>
        </div>
        <div class="col-3">
            <div class="form-floating">
                <input name="node2" id="nodeid2_${id}" type="text" class="form-control" required pattern="\\d+">
                <label class="form-label" for="floatingInputGroup1">NodeId2</label>
            </div>
        </div>
        <div class="col my-auto">
            <button type="submit" id="aligner_align_${id}" class="btn btn-primary">Align</button>
        </div>
    </form>
    <div class="result_holder"></div>
</div>
`;
        this.holder = holder.querySelector(".vizbody");
        holder.querySelector(`#aligner_close_${id}`).addEventListener("click", function(){
            holder.remove(); 
        });

        let cardbody = holder.querySelector(".vizbody");

        holder.querySelector('form').addEventListener("submit", async function (event) {
            event.preventDefault();
            let data = new FormData(this);
            let nodeid1 = parseInt(data.get("node1"));
            let nodeid2 = parseInt(data.get("node2"));

            let alignment = await G.api.get.align(G.gname, nodeid1, nodeid2);
            


            let result_holder = cardbody.querySelector(".result_holder");
            result_holder.innerHTML = "";
            result_holder.classList.add("overflow-x-scroll", "p-3");
            let score = document.createElement("div");
            score.innerHTML="Score: " + alignment.score;
            result_holder.appendChild(score);

            let seq1 = alignment.align_seq1.map(char => char == null ? "-" : char);

            let seq2 = alignment.align_seq2.map(char => char == null ? "-" : char);

            let seq1handler = document.createElement("div");
            seq1handler.classList.add("text-nowrap");

            let seq2handler = document.createElement("div");
            seq2handler.classList.add("text-nowrap");

            let interSeqHandler = document.createElement("div");
            interSeqHandler.classList.add("text-nowrap");

            seq1handler.style.fontFamily = "monospace";
            interSeqHandler.style.fontFamily = "monospace";
            seq2handler.style.fontFamily = "monospace";

            for (var i = 0; i < seq1.length; i++) {
                let A = seq1[i];
                let B = seq2[i];

                seq1handler.innerHTML += A;
                seq2handler.innerHTML += B;
                
                if (A == B) {
                    interSeqHandler.innerHTML += '<span class="align-valid">|</span>';
                } else {
                    interSeqHandler.innerHTML += '<span class="align-invalid">&nbsp</span>';
                }
            }

            result_holder.appendChild(seq1handler);
            result_holder.appendChild(interSeqHandler);
            result_holder.appendChild(seq2handler);

        })
        this.container.prepend(holder);
        this.setUpListeners();

        return this;
    }

    setUpListeners() {
        let that = this;
        let rows = this.linked_table.returnRows();
        rows.forEach((row) => {
            let idtd = row.querySelector("td")
            idtd.addEventListener("click", function () {
                that.fillInput(idtd.textContent);
            })
        });
    }

    fillInput(inputNodeID) {
        let nodeid1 = this.container.querySelector('#nodeid1_' + this.id);
        let nodeid2 = this.container.querySelector('#nodeid2_' + this.id);

        if (nodeid1.value == null) {
            nodeid1.value = inputNodeID;
        }
        
        else if (nodeid1.value != null && nodeid2.value == null) {
            nodeid2.value = inputNodeID;
        }

        else {
            nodeid2.value = nodeid1.value;
            nodeid1.value = inputNodeID;
        }
    }
}
