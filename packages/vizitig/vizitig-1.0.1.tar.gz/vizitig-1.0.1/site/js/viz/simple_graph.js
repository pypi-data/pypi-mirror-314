import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import { BaseViz } from "../visualisation.js";
import { Highlight, ShowId, Scale, Tag, Transparency} from "../viz_actions/d3_actions.js";
import { Hide } from "../viz_actions/default_actions.js";
import { default_prop } from "../d3_default.js";
import { PARTIALLY } from "../config.js";
import { dl_svg, create_svg, hand, move, file_svg } from "../utils.js";

const translate_attr = /(.*)translate\([^()]*\)(.*)/ // allow to remove translate(...) from a transform attr
function remove_translate(attr){
    let m = attr.match(translate_attr);
    if (m == null)
        return attr
    return m.splice(1).join("");
}

export class D3Viz extends BaseViz{
    width = "100%";
    height = "100%";

    get_container(container) {
        return container;
    }

    constructor(graph, container, properties){
        super(graph, container);
        this.d3_propr = {};
        this.init_posX = 0;
        this.init_posY = 0;
        this.init_scale = 1;
        Object.assign(this.d3_propr, default_prop);
        if (properties != undefined)
            Object.assign(this.d3_prowpr, properties);
    }

    get_state(){
        let state = super.get_state();
        let transform = this.g.node().transform.baseVal.consolidate();
        state.args.init_posX = transform.matrix.e;
        state.args.init_posY = transform.matrix.f;
        state.args.init_scale = transform.matrix.a;
        return state;
    }


    delete_selection(){
        if (this.selection != undefined){
            delete this.selection;
            this.svg.on("click", ()=>{}); 
            this.svg.on("mousemove", ()=>{}); 
        }
        this.svg.selectAll(".select_group").remove();
    }

    extra_header(){
        let extra = this.holder.querySelector(".header-buttons");
        let form = document.createElement("form");
        form.classList.add("btn-group", "mx-1");
        form.setAttribute("role", "group");
        form.innerHTML = `
  <input id="vizhand_${this.viz_id}" type="radio" class="btn-check" name="pointer_action" value="hand" autocomplete="off">
  <label class="btn btn-secondary-outline" for="vizhand_${this.viz_id}">${hand}</label>

  <input type="radio" class="btn-check" name="pointer_action" id="vizmove_${this.viz_id}" value="move" autocomplete="off" checked>
  <label class="btn btn-secondary-outline" for="vizmove_${this.viz_id}">${move}</label>
`;
        let that = this;
        form.onchange = () => that.draw();
        this.pointer_action_form = form;
        let button = document.createElement("button");
        button.setAttribute("id", `vizsvg_${this.viz_id}`);
        button.classList.add("btn", "btn-sm", "btn-outline-secondary");
        button.innerHTML = file_svg;
        button.onclick = function(){
            dl_svg(that.svg.node());
        };

        extra.prepend(button);
        extra.prepend(form);

    }
    get actions(){
        return [ShowId, Scale, Tag, Transparency, Highlight, Hide];
    }

    get post_default_actions(){
        return [
            ["selection", new Highlight(this.graph, {filter: "selection", color:"blue"})]
        ]
    }

    get vizname(){
        return "Simple graph";
    }

    build_svg(){
        if (this.svg != undefined)
            return
        this.body.innerHTML = "";
        this.svg = d3.select(this.body).append("svg")
            .attr("width", this.width)
            .attr("height", this.height)
            .style("background-color", "rgb(232, 232, 232)");
            //.attr("viewBox", `${-this.width/2} ${-this.height/2} ${this.width} ${this.height}`); 
        let g = this.g = this.svg.append("g")
                .attr("transform", `translate(${this.init_posX}, ${this.init_posY}) scale(${this.init_scale})`);
        this.zoom = d3.zoom().scaleExtent([0.1, 4]);
        this.zoom.on("zoom", (event) => { g.attr("transform", event.transform) });
        this.svg.call(this.zoom);
        this.svg.call(this.zoom.transform, d3.zoomIdentity.translate(this.init_posX, this.init_posY).scale(this.init_scale));
    }

    get pointer_action(){
        return new FormData(this.pointer_action_form).get("pointer_action");
    }

    prepare(){
        let that = this;
        this.build_svg();
        this.g.append("line")
            .attr("x1", "-1000")
            .attr("y1", "0")
            .attr("x2", "1000")
            .attr("y2", "0")
            .attr("stroke", "grey");
        this.svg.on(".zoom", null);
        this.svg.style("cursor", ""); 
        this.delete_selection();
        if (this.pointer_action == "move") {
            this.svg.style("cursor", "move"); 
            this.svg.call(this.zoom);
        }
        if (this.pointer_action == "hand"){
            this.selection = {};
            build_selection_tool(that);
        }
        if (this._nodes_map == undefined)
            this._nodes_map = new Map(); 
        if (this._nodes == undefined)
            this._nodes = []; 
        for (const [nid, data] of this.graph.nodes_with_data){
            if (this._nodes_map.has(nid)){
                let nid_data = this._nodes_map.get(nid)
                if (nid_data.g != undefined)
                    nid_data.g.remove();
                nid_data.g = undefined;
                nid_data.data = data;
                continue;
            }
            let cdata = {id: nid, data:data};
            this._nodes_map.set(nid, cdata);
            this._nodes.push(cdata);
        }

        this._edges = [];
        this.g.selectAll("line").remove();
        for (const [source, target] of this.edges){
            this._edges.push({source: source, target:target});
        }
        if (this.simulation == undefined)
            this.simulation = d3.forceSimulation();
        this.simulation.nodes(this._nodes);
        this.simulation 
            .alpha(this.d3_propr.alpha)
            .alphaDecay(this.d3_propr.alpha_decay)
            .force("link", d3.forceLink(this._edges).id(d=>d.id).strength(this.d3_propr.link_strength))
            .force("center", d3.forceCenter(0, 0).strength(1)) 
            .force("charge", d3.forceManyBody(this.d3_propr.charge_strength).distanceMax(this.d3_propr.charge_radius))
            .on("tick", ()=>that.update()).restart();
    }
    end_update(){
        this.g.selectAll(".node").call(drag(this));
    }

    get nodes(){
        return this._nodes_map.keys(); 
    }

    draw_node(node){
        let data = this._nodes_map.get(node);
        if (data.g == undefined){
            let g = d3.create("svg:g");
            g.attr("fill", "white")
             .attr("class", "node");
            if (data.data.seq != undefined){
                let width =  10 + Math.sqrt(data.data.seq.length - this.graph.k);
                g.append("rect")
                    .attr("width", width)
                    .attr("height", 10)
                    .attr("rx", 3)
                    .attr("stroke", "black")
                    .attr("transform", `translate(-${width/2}, -5)`);
            }
                    
            else
                g.append("circle")
                 .attr("r", 5)
                 .attr("stroke", "black");
            let sub = g.append("g");
            sub.attr("class", "add_info");
            data.g = g;
        }
        data.g.style("cursor", "pointer");
        data.g.attr("class", "nodeg");
        let sub = data.g.select(".add_info");
        sub.selectAll("*").remove();
        data.g.attr("transform", "");
        data.g.attr("nid", node);
        data.g.call(drag(this, data));
        let that = this;
        data.g.on("click", function(event){
            if (that.pointer_action == "move")
                data.px=data.py=undefined
            else{
                that.graph.select_nodes([node]);
                event.stopPropagation(); // prevent the selection rectangle to be triggered
            }
        });
        return data.g;
    }
    draw_edge(source, target){
        let line = d3.create("svg:line")
            .attr("stroke", "black");
        return line;
    } 

    attach_node(node){
        this.g.append(()=>node.node());
    }

    attach_edge(edge){
        this.g.append(()=>edge.node());
    }

    update_node(node, element){
        let data = this._nodes_map.get(node);
        let tr = remove_translate(element.attr("transform"));
        let x = (data.px!=undefined) ? data.px :data.x;
        let y = (data.py!=undefined) ? data.py :data.y;
        data.x = x;
        data.y = y;
        element.attr("transform", `translate(${x},${y}) ${tr}`);
    }
    update_edge(source, target, element){
        let source_data = this._nodes_map.get(source);
        let target_data = this._nodes_map.get(target);
        element.attr("x1", source_data.x)
            .attr("y1", source_data.y)
            .attr("x2", target_data.x)
            .attr("y2", target_data.y);
    }
}


function drag(graph, data){
    function dragstarted(event) {
        if (graph.pointer_action == "move")
        data.px = data.py = undefined;
    }
    function dragged(event) {
        if (graph.pointer_action == "move"){
            graph.simulation.alpha(graph.d3_propr.alpha).restart();
            data.px = event.x;
            data.py = event.y;
        }
    }
    function dragended(event) {
    }
    return d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended);
}

function build_selection_tool(graph_viz){
    graph_viz.svg.on("click", function(event){
        if (graph_viz.selection.g == undefined){
            graph_viz.selection.g = graph_viz.g.append("g");
        }
        if (graph_viz.selection.posX == undefined){
            graph_viz.selection.g = graph_viz.g.append("g").attr("class", "select_group");
            var xy = d3.pointer(event);
            var transform = d3.zoomTransform(graph_viz.svg.node());
            xy = transform.invert(xy);
            graph_viz.zoom
            graph_viz.selection.posX = xy[0];
            graph_viz.selection.posY = xy[1];
            graph_viz.selection.g.append("circle")
                    .attr("cx", xy[0])
                    .attr("cy", xy[1])
                    .attr("r", 5)
                    .style("fill", "grey");
            graph_viz.selection.g.append("rect")
                    .attr("x", xy[0])
                    .attr("y", xy[1])
                    .attr("fill", "blue")
                    .attr("opacity", "0.3")
                    .attr("width", 0)
                    .attr("height", 0);
        }
        else {
            let selected_nodes = []
            for (const data of graph_viz._nodes){
                if ((graph_viz.selection.posX < data.x & data.x < graph_viz.selection.posX + graph_viz.selection.width) &
                   (graph_viz.selection.posY  < data.y & data.y < graph_viz.selection.posY + graph_viz.selection.height))
                    selected_nodes.push(data.id);
            }
            graph_viz.graph.select_nodes(selected_nodes);
            delete graph_viz.selection.posX;
            delete graph_viz.selection.posY;
        }
        
    });
    graph_viz.svg.on("mousemove", function(event){
        if (graph_viz.selection.g != undefined){
            var xy = d3.pointer(event);
            var transform = d3.zoomTransform(graph_viz.svg.node());
            xy = transform.invert(xy);
            let width  = graph_viz.selection.width = xy[0] - graph_viz.selection.posX;
            let height = graph_viz.selection.height= xy[1] - graph_viz.selection.posY;
            graph_viz.selection.g.select("rect").attr("width", width)
                                    .attr("height", height);
        }
    });
    
}
