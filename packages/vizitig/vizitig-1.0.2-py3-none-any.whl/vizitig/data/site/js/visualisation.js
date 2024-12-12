import { modal } from "./ui.js";
import {Hide, Highlight} from "./viz_actions/default_actions.js";
import {rand_str} from "./utils.js";

///// VIZ SPEC ///////


// * keyname
// * prepare
// * draw_nodes
// * draw_edges
// * finish
// * Action of available list:
//      - name
//      - form for arguments
//      - filter function
//      - transform function

let viz_id = 0;

export class BaseViz {
    #viz_id;
    #action_inst;
    constructor(graph){
        this.graph = graph;
        this.holder_width = "";
        this.holder_height = "45vh";
        this.container = main;
        this.#action_inst = new Map();
        this.#viz_id = viz_id;
        viz_id += 1;
    }

    get_state(){
        return {
            actions: [...this.#action_inst.values()].map(e => e.get_state()),
            vizname: this.vizname,
            args: {
                holder_width: this.holder.clientWidth+"px",
                holder_height: this.holder.clientHeight+"px",
            }
        }
    }

    static from_state(graph, obj){
        let res = new this(graph, obj.args)
        Object.assign(res, obj.args);
        res.build();
        for (const action of obj.actions){
            let actType = res.action_by_key(action.type);
            let formData = new FormData();
            Object.entries(action.args).forEach( (kv) => formData.set(kv[0], kv[1]))
            let act = new actType(graph, formData);
            res.add_action(act); 
        }
        return res;
    }

    get viz_id(){
        return this.#viz_id;
    }

    get pre_default_actions(){
        return [];
    }
    get post_default_actions(){
        return [];
    }
    get actions(){
        return [Hide, Highlight];
    }

    get action_inst(){
        let arr = [... this.pre_default_actions]
        arr.push(...this.#action_inst.entries());
        arr.push(...this.post_default_actions)
        return new Map(arr); 
    }

    get _actions(){
        let actions = [];
        if (super._actions != undefined)
            actions = actions.concat(this._actions);
        actions = actions.concat(this.actions);
        return actions;
    }

    action_by_key(key){
        return this._actions.filter(e => e.name == key)[0]
    }

    build(){
        let holder = document.createElement("div");
        holder.classList.add("col-6", "border", "card", "p-0", "overflow-hidden", "m-1");
        holder.style.height = this.holder_height;
        holder.style.width = this.holder_width;
        holder.style.resize = "both";
        holder.setAttribute("id", `viz_${this.viz_id}`);
        
        holder.innerHTML = `
<div class="vizhead card-header  p-1">
    <div class="p-0 vizmenu_main">
         <div class="container-fluid d-flex "> 
             <span>
                <h5>${this.vizname}</h5>
             </span>
             
             <span class="header-buttons ms-auto d-flex" id="button_span_${this.viz_id}"> 
                    
                 <button type="button" class="btn viz-toggle navbar-toggler my-auto mx-2" data-bs-toggle="collapse" data-bs-target="#vizmenu_${this.viz_id}_new">
                    Add action
                 </button>
                 <button type="button" class="btn viz-toggle navbar-toggler my-auto mx-2" data-bs-toggle="collapse" data-bs-target="#vizmenu_${this.viz_id}_actions">
                    Show actions
                 </button>
                 <button class="viz-close btn-close my-auto" aria-label="Close"></button>
             </span>
        </div>
        <div id="vizmenu_${this.viz_id}_actions" class="vizmenu setup_action_list container-fluid collapse border-top">
            <form class="row py-1 list_action form">
                <div class="col-3">
                    <div class="form-floating">
                        <select class="form-select" id="action_list_select_${this.viz_id}"></select>
                        <label class="form-label" for="action_list_select_${this.viz_id}"> List of actions</label>
                    </div>
                </div>
                <div class="col  d-flex">
                    <input type="button" class="btn btn-danger delete ms-auto my-auto" value="remove">
                </div> 
            </form>
        </div>

        <div id="vizmenu_${this.viz_id}_new" class="vizmenu container-fluid collapse border-top">
            <form class="add_action form row">
                <span class="col-3 my-1">
                    <div class="form-floating">
                        <select id="filter_list_${this.viz_id}" class="filter_list form-select" name="filter">
                        </select>
                        <label class="form-label" for="filter_list_${this.viz_id}"> Apply a filter</label>
                    </div>
                </span>
                <span class="col-1 d-flex">
                    <input class="form-check-input my-auto" type="checkbox" name="not" value="" id="flexCheckChecked">
                    <label class="form-label my-auto mx-2"> not </label>
                </span>
                <span class="col-3 my-1">
                    <div class="form-floating">
                        <select class="action_list form-select" id="action_list_${this.viz_id}">
                        </select>
                        <label class="form-label" for="action_list_${this.viz_id}">Action</label>
                    </div>
                </span>
                <span class="col d-flex">
                    <input type="submit" class="btn btn-primary ms-auto my-auto" value="Apply">
                </span>
            </form>
        </div>
    </div>
</div>
<div class="vizbody card-body p-0 mh-100 overflow-auto"></div>
`;
        this.container.prepend(holder);
        this.holder = holder;
        let that = this;

        // build the filter list 
        this.update_filter();

        // viz deps header construction
        this.extra_header();

        // build the action list
        let action_list = holder.querySelector(".action_list");
        for (const act of this._actions){
            let opt = document.createElement("option");
            opt.value = opt.innerHTML = act.name;
            action_list.appendChild(opt);
        }

        // logic to expose form of each action
        let action_form = this.holder.querySelector(".add_action");
        action_list.onchange = function(){
            [...action_form.querySelectorAll(".extra_form")].forEach(e=>e.remove()); // delete extra form element 
            let act = that.action_by_key(this.value);

            that.current_action = act;
            act.form(action_form);
        }
        action_list.onchange();

        // Toggle menu
        //This.holder.addEventListener("mouseenter", function(){
        //    that.holder.querySelector(".vizmenu_main").classList.add("show");
        //});
        //This.holder.addEventListener("mouseleave", function(){
        //    that.holder.querySelector(".vizmenu_main").classList.remove("show");
        //});

        // add_action logic
        let add_action = this.holder.querySelector(".add_action");
        add_action.addEventListener("submit", function(event){
            event.preventDefault();
            const formData = new FormData(this);
            let act_inst = new that.current_action(that.graph, formData);
            that.add_action(act_inst);
        });

        // linking field with html nodes
        this.head = holder.querySelector(".vizhead");
        this.body = holder.querySelector(".vizbody");
        let menu = this.menu = holder.querySelector(".vizmenu");


        // closing the viz
        holder.querySelector('.viz-close').addEventListener("click", function(){
            that.graph.delete_onready_callback(that.draw_callback);
            holder.remove(); 
            that.graph.remove_viz(that);
        });

        // callback logic
        this.draw_callback = () => that.draw();
        this.update_filter_callback = () => that.update_filter();
        this.graph.add_onready_callback(this.draw_callback);
        this.graph.add_onupdate_filter_callback(this.update_filter_callback);
        this.draw();
    }

    extra_header(){}

    add_action(action_instance){
        let that = this;
        let actid = rand_str();
        this.#action_inst.set(actid, action_instance);
        let select = this.holder.querySelector(".setup_action_list select");
        let form = this.holder.querySelector(".setup_action_list form");
        let option = document.createElement("option");
        option.value = actid; 
        option.innerHTML = `${action_instance.filter_key}:${action_instance.constructor.name}`;
        select.appendChild(option);
        select.onchange = function(){
            [...form.querySelectorAll(".extra_form")].forEach( e => e.remove() );
            let selected_option = select.selectedOptions[0];
            if (selected_option == undefined) return;
            let sel_id = selected_option.value;
            let action_instance = that.action_inst.get(sel_id);
            action_instance.constructor.form(form);
            for (const [key, val] of action_instance.args.entries())
                if (form.elements[key] != undefined){
                    form.elements[key].value = val;
                    form.elements[key].onchange = function(){
                        for ( const [key, val] of new FormData(form).entries())
                            action_instance.args.set(key, val);
                        that.draw();  
                    }
                }
            let close = form.querySelector(".delete");
            close.onclick = function(){
                that.action_inst.delete(sel_id);
                selected_option.remove();
                that.draw();
                select.onchange();
            }
        }
        select.onchange();
    
        //li.querySelector("button").onclick = () => {
        //    li.remove();
        //    that.action_inst.delete(action_instance);
        //    that.draw();
        //}
        this.draw();
        

    }

    update_filter(){
        let filter_list = this.holder.querySelector(".filter_list");
        filter_list.innerHTML = "";
        for (const filter of this.graph.filters){
            let opt = document.createElement("option");
            opt.value = opt.innerHTML = filter;
            filter_list.appendChild(opt);
        }
    }

    get vizname(){
        return "BaseViz";
    }

    get nodes(){
        return this.graph.nodes;
    }

    get edges(){
        let edges = [];
        for (const [source, target] of this.graph.edges){
            let is_filtered = false;
            for (const act of this.action_inst.values())
                if (!(act.filter(source) & act.filter(target))){
                    is_filtered = true;
                    break;
                }
            if (is_filtered)
                continue;
            edges.push([source, target])
        }
        return edges; 
    }

    prepare(){}
    start_update(){}
    end_update(){}
    finish(){}
    draw_node(node){}
    draw_edge(source, target){}
    attach_node(drawn_node){}
    attach_edge(drawn_edge){}
    permut_nodes(nodes){return nodes}

    draw(){
        console.log(`Drawing ${this.vizname}`);
        this.prepare();
        this._draw();
        this.finish();
        this.update();
        this.graph.state_in_url();
    }

    _draw(){
        this.start_update();
        let nodes = this.permut_nodes(this.nodes);
        this.nodes_drawing = [];
        this.edges_drawing = [];
        for (const node of nodes){
            let is_filtered = false;
            for (const act of this.action_inst.values())
                if (!act.filter(node)){
                    is_filtered = true;
                    break;
                }
            if (is_filtered)
                continue;
            let draw_node = this.draw_node(node);
            if (draw_node == undefined)
                continue
            this.nodes_drawing.push([node, draw_node]);
            for (const act of this.action_inst.values()){
                draw_node = act.transform_node(node, draw_node);
            }
        }
        for (const [source, target] of this.edges){
            let draw_edge = this.draw_edge(source, target);
            if (draw_edge == undefined)
                continue
            
            for (const act of this.action_inst.values()){
                draw_edge = act.transform_edge(source, target, draw_edge);
            }
            this.edges_drawing.push([source, target, draw_edge]);
        }

        for (const [source, target, draw_edge] of this.edges_drawing)
            this.attach_edge(draw_edge); 

        for (const [nodeid, draw_node] of this.nodes_drawing)
            this.attach_node(draw_node); 
        this.end_update();
    }
    update_node(node, element){}
    update_edge(source, target, element){}
    update(){
        for (const [node, draw_node] of this.nodes_drawing){
            this.update_node(node, draw_node);
            //for (const act of this.action_inst)
            //    act.transform_node(node, draw_node);
        }
        for (const [source, target, draw_edge] of this.edges_drawing){
            this.update_edge(source, target, draw_edge);
            //for (const act of this.action_inst)
            //    act.transform_edge(source, target, draw_edge);
        }
    }
}

