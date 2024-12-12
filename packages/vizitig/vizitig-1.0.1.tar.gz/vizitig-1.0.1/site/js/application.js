import {API} from "./api.js";
import {PARTIALLY, API_HREF} from "./config.js";

// Overall datastructure //
//
// Nodes are represented by their node id.
// The applications follows the nx data structure.
// Nodes can be in two states:
//  - fully loaded from the backend
//  - partially loaded from the backend 
// This distinction is required to not load all the graph
// from the backend into the front end.
//
//
// Edges are a Map of Map to object where the object contains the
// edge description (signature of BCALM, and other informations found in the nx Graph).
//
// Metadata Description are an object aligned with the spec of the metadata python project.
//
// On the top of that, we have Tags that is a named query of the DSL. A Tag will matched
// all fully_loaded nodes (and only them, not the other one) dynamically.
// all partially_loaded nodes must be connected to at least one fully_loaded nodes.
//
// A Visualisation of the graph should hook the onready_callback. 

export class Graph{
    #gname;
    #metadata; 
    #nodes; 
    #adj;
    #logger;
    #filters;
    #onready_callback;
    #onupdate_filter_callback;
    #selection;
    #viz_list;

    // gname is the string name of the graph
    // logger is a Logger object
    constructor(gname, logger){
        this.#gname = gname;
        this.#nodes = new Map(); // nid to Node properties 
        this.#adj = new Map(); // nid to nid to edge properties
        this.api = new API(API_HREF, logger); 
        this.#logger = logger; 
        this.#viz_list = [];
        this.#filters = new Map(); 
        this.#selection = new Set();
        this.#onready_callback = new Set(); // callback when the graph has finished some maintenance operations after modification.
        this.#onupdate_filter_callback = new Set(); // callback when the graph has update its set of filter.
        this.add_onupdate_filter_callback(()=>this.state_in_url());
        this.add_onready_callback(()=>this.state_in_url());
        let that = this;
    }
    async build(){
        await this.api.build();
        this.api.get.version().then(v=>version.innerHTML = v);
        let that = this;

        // default filters
        this.parse_query("ALL()").then( ast => that.add_filter("all", ast));
        this.parse_query("Partial()").then( ast => that.add_filter("partial nodes", ast));
        this.parse_query("Selection()").then( ast => that.add_filter("selection", ast));
        this.parse_query("Degree(1)").then( ast => that.add_filter("tips", ast)); // the name is choosen by Camille. I declined all responsabilities.
        // end of default filters

        this.#metadata = await this.api.get.graph_info(this.gname);
        this.api.get.get_export_format().then(function(L){
            for (const format of L){
                let option = document.createElement("option");
                option.innerHTML = option.value = format;
                export_format_list.appendChild(option);
            }
        }); 
        this.add_onupdate_filter_callback(function(graph){
            export_filter_list.innerHTML = ""; 
            for (const filter of graph.filters){
                let option = document.createElement("option");
                option.innerHTML = option.value = filter;
                export_filter_list.appendChild(option);
            } 
        });
        this.list_filters().then(Lfilters => Lfilters.map(e => that.add_filter_str(e[0], e[1])));
        this.onupdate_filter();

        console.log('Finished building graph.');
    }

    // Return an object representaiton of the state of the application
    get_state(){
        return {
                gname: this.#gname,
                nodes: [...this.#nodes.keys()], 
                selection: [...this.#selection.keys()],
                viz: this.#viz_list.map(e => e.get_state())
        }
    }

    state_in_url(){
        let state = this.get_state();
        let enc_state = btoa(JSON.stringify(state));
        let url = new URL(window.location.href);
        window.history.replaceState(state, null, `graph.html?state=${enc_state}`);
        
    }

    static async from_state(obj, logger){
        let G = new this(obj.gname, logger);
        await G.build();
        let promises = obj.viz.map(v => G.restore_viz(v));
        await Promise.all(promises);
        G.select_nodes(obj.selection);
        let query = `OR(${obj.nodes.map(e=>`NodeId(${e})`).join(',')})`;
        console.log(query);
        await  G.fetch_nodes(query);
        return G;
    }

    static async load_vizmodule(key){
        let module = await import(`./viz/${key}.js`);
        let arr = Object.values(module); 
        if (arr.length > 1)
            this.logger.error(`viz/${key}.js should contains only one exported element`);       
        return arr[0]
    }

    async add_viz(key){
        let vizclass = await this.constructor.load_vizmodule(key);
        let viz = new vizclass(this);
        await viz.build();
        this.#viz_list.push(viz);
        this.state_in_url();
        return viz;
    }

    async restore_viz(obj){
        let vizclass = await this.constructor.load_vizmodule(obj.vizname.toLowerCase().replace(" ", "_"));
        let viz = vizclass.from_state(this, obj);
        this.#viz_list.push(viz);
        return viz;
    }

    get viz_list(){
        return this.#viz_list;
    }

    remove_viz(viz){
        this.#viz_list.splice(this.#viz_list.indexOf(viz), 1);
        this.state_in_url();
    }

    get k(){
        return this.#metadata.k;
    }

    get metadata_types_list(){
        return this.#metadata.types_list;
    }

    get metadata_vars_values(){
        return this.#metadata.vars_values;
    }

    get nodes(){
        return [... this.#nodes.keys()];
    }

    get nodes_with_data(){
        return this.#nodes.entries();
    }

    get total_size(){
        return this.#metadata.size;
    }

    node_data(nid){
        return this.#nodes.get(nid);
    }

    get gname(){
        return this.#gname;
    }

    add_onready_callback(callback){
        this.#onready_callback.add(callback); 
    }

    delete_onready_callback(callback){
        this.#onready_callback.delete(callback);
    }

    add_onupdate_filter_callback(callback){
        this.#onupdate_filter_callback.add(callback); 
    }

    delete_onupdate_filter_callback(callback){
        this.#onupdate_filter_callback.delete(callback); 
    }

    get fully_loaded_nodes(){
        return [...this.#nodes.entries()].filter(e => e[1] != PARTIALLY).map(e=>e[0]);
    }

    get partially_loaded_nodes(){
        return [...this.#nodes.entries()].filter(e => e[1] == PARTIALLY).map(e=>e[0]);
    }

    // Fully load all nodes in nodes.
    async expand_nodes(nodes){
        let node_desc = await this.api.get.nodes_data(this.gname, nodes)
    }

    // add node data list of (nid, NodeDesc)
    add_nodes(node_data){
        for (const [nid, desc] of node_data){
            this.#nodes.set(nid, desc);
            if (!this.#adj.has(nid))
                this.#adj.set(nid, new Map());
            let neighbors_nid = this.#adj.get(nid);
            for (const [oid_base, odesc] of Object.entries(desc.neighbors)){
                let oid = parseInt(oid_base);
                if (!this.#nodes.has(oid))
                    this.#nodes.set(oid, PARTIALLY);
                neighbors_nid.set(oid, new Map());
            }
        }
        this.onready();
    }

    get edges(){
        return this._edges()
    }
    * _edges(){
        for (const x of this.#adj.keys())
            for (const y of this.#adj.get(x).keys())
                yield [x, y];
    }

    // execute the query and fully load all the nodes and edges
    async fetch_nodes(query){
        this.add_nodes(await this.api.get.find_with_query(this.gname, query));
    }

    // toggle nodes to partially_loaded
    delete_nodes(nodes){
        for (const nid of nodes){
            this.#nodes.set(nid, PARTIALLY);
        }
        this.clean_graph();
        this.onready();
    }

    select_nodes(nodes){
        this.#selection = new Set(nodes);
        this.onready();
    }

    // Delete partially loaded nodes connected to only partially loaded nodes
    clean_graph(){
        for (const nid of this.partially_loaded_nodes){
            let neighbors = [... this.#adj.get(nid).entries()]
            if (neighbors.every(e=>that.#nodes.get(e) == PARTIALLY)){
                this.#adj.delete(nid);
                this.#nodes.delete(nid);
                for (const oid of neighbors){
                    this.#adj.get(oid).delete(nid);
                }
            }
        }
    }

    onready(){
        let that = this;
        this.#onready_callback.forEach(f=>f(that));
    }

    onupdate_filter(){
        let that = this;
        this.#onupdate_filter_callback.forEach(f=>f(that));
    }
        
    async parse_query(query_str){
        return await this.api.get.parse_query(this.gname, query_str);
    }

    async list_filters(){
        return await this.api.get.list_filters(this.gname);
    }

    add_filter(key, query_ast){
        if (Object.keys(query_ast).length == 0) // empty object
            this.#filters.delete(key);
        else
            this.#filters.set(key, query_ast);
        this.onupdate_filter();
    }

    async add_filter_str(key, query_str){
        let ast;
        if (query_str.trim() == "")
            ast = {}; 
        else
            ast = await this.parse_query(query_str);
        this.add_filter(key, ast);
    }

    get filters(){
        return [...this.#filters.keys()]
    }

    remove_filter(key){
        this.#filters.remove(key);
    };

    _node_satisfy(ast, nodeid){
        let that = this;
        let keys = Object.keys(ast);
        let key;
        let name = undefined;
        if (keys.length > 1){
            if (ast.name == undefined || ast.type == undefined)
                throw new Error("AST should have at most one key");
            name = ast.name.toLowerCase();
            key = ast.type.toLowerCase();
        } else 
            key = keys[0].toLowerCase();
        if (key == "land" )
            return ast.land.map((e) => that._node_satisfy(e, nodeid)).every(e=>e);
        if (key == "lor")
            return ast.lor.map((e) => that._node_satisfy(e, nodeid)).some(e=>e);
        if (key == "lnot")
            return ! this._node_satisfy(ast.lnot, nodeid)
        if (key == "id")
            return nodeid == ast[key]; 
        if (key == "all")
            return true; 
        if (key == "selection")
            return this.#selection.has(nodeid);
 

        let data = this.#nodes.get(nodeid);
        if (key == "partial")
            return data == PARTIALLY;
        if (data == PARTIALLY)
            return false;
        if (key == "degree")
            return Object.keys(data.neighbors).length == ast[key];
        if (name == undefined)
            name = ast[key].toLowerCase()
        for (const metadata of this.#nodes.get(nodeid).metadatas)
            if (metadata.type.toLowerCase() == key && metadata.id.toLowerCase() == name)
                return true;
        return false;
    }

    node_satisfy(key, nodeid){
        if (!this.#filters.get(key))
            throw new Error(`Unkown filter key: ${key}`);
        return this._node_satisfy(this.#filters.get(key), nodeid);
    }

    all_nodes_satisfying(key){
        let that = this;
        return this.nodes.filter((e) => that.node_satisfy(key, e));
    }

    export_current(format){}
    
}
