import { MetaViz } from "./metadata.js";
import { FiltersManager, filter_instances } from "./filters.js";
import {Hide} from "./viz_actions/default_actions.js";
import { chunkArray } from "./utils.js";

let default_viz_open = new Map();
default_viz_open.set("simple_graph", 
{
    "style": {width: "66vw", height: "85vh"},
    "actions": []
}
    );
default_viz_open.set("table", {
    "style": {width: "32vw", height: "85vh"},
    "actions":
        [
            (graph) => new Hide(graph, {filter: "selection", not: true})
        ]
}
);



export function set_page(G, load_default_viz){
    refresh.href = `graph.html?graph=${G.gname}`;
    for (const el of document.querySelectorAll("[gname]")){
        el.innerHTML += G.gname; 
    }
    total_size.innerHTML = G.total_size;

    //Add data injection here
    G.add_onready_callback(async function(){
        fetched_nodes.innerHTML = G.fully_loaded_nodes.length;
        discovered.innerHTML = G.nodes.length;
    });
    

    G.api.get.load_viz().then(async function(vizlist){
            for (const vizname of vizlist.sort().reverse()){
                let li = document.createElement("li");
                li.innerHTML = `<a class="dropdown-item href="#">${vizname.replace("_", " ")}</a>`;
                li.onclick = () => G.add_viz(vizname);
                vizlist_holder.appendChild(li);
                if (default_viz_open.has(vizname) && load_default_viz){
                    let viz = await G.add_viz(vizname)
                    for (const [key, value] of Object.entries(default_viz_open.get(vizname).style))
                        viz.holder.style[key] = value;
                    for (const act of default_viz_open.get(vizname).actions)
                        viz.add_action(act(G)); 
                }
            }
    });
    fetch_node.addEventListener("submit", async function(event){
        event.preventDefault();
        const formData = new FormData(this);
        let query_str = formData.get("query");
        let action = event.submitter.value;
        //fetch_node.querySelector("button[type=submit]").setAttribute("disable");
        if (action == "fetch")
            G.fetch_nodes(query_str).finally(()=>fetched_nodes.disabled = false);
        if (action == "expand"){
            
            let P = []
            for (const chunk of chunkArray(G.partially_loaded_nodes.map(e=>`NodeId(${e})`), 20)){
                let query_str = `OR(${chunk.join(",")})`;
                if (query_str.length != 0)
                    await G.fetch_nodes(query_str);
            } 
            fetched_nodes.disabled = false;
        }
    });

    export_form.addEventListener("submit", async function(event){
        event.preventDefault(); 
        const formData = new FormData(this);
        let filter = formData.get("filter");
        G.api.post.export_nodes(G.gname, formData.get("format"), G.all_nodes_satisfying(filter)).then(function(url){
            /// shameless stolen from https://stackoverflow.com/a/23013574
            var link = document.createElement("a");
            link.setAttribute("target", "_blank");
            link.setAttribute("download", "");
            link.href = url;
            document.body.appendChild(link);
            link.click();
            link.remove();
        })
    });
    const metadataselector = document.getElementById("metadata_manager_button");
    metadataselector.onclick = () => (new MetaViz(G)).build();

    const filtermanager = document.getElementById("filter_manager_button");
    filtermanager.onclick = () => (new FiltersManager(G)).build();

    add_filter_button.addEventListener("click", function() {
        G.add_filter_str(filterName.value, queryField.value.trim());
        G.api.post.add_filter(G.gname, filterName.value, queryField.value);
        filternameinput.classList.remove("show");
        filter_instances.forEach(element => {
            element.refresh_table();
        });
    })


    // filter_manager_button.addEventListener("click", function() {
    //     filters = G.api.get.get_filters();
    //     console.log(filters);
    // })
        
}






export function setUpDSLButtonFunctions() {
    console.log('Seeting up DSL button listeners.');
    queryField = document.querySelector("#queryField");
    for (const button in Object.entries(document.querySelector(".DSLButton"))){
        button.addEventListener('click', () => function() {
            queryField.value += button.valueOf})
        }
    }


function addMetadataToQuery(element) {
    queryField = document.querySelector('#queryField');
    var str = element.type + '(' + element.id + ') ';
    queryField.value += str;
}

// create a meta element from a DOM detached element
export function modal(content){
    // TODO
}

export function autoResizeQueryField() {
    console.log("Resizing");
    queryField.style.height = "auto";
    queryField.style.height = queryField.scrollHeight + 'px';
}

