import {Graph} from "./application.js";
import {Logger} from "./logger.js";
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import {set_page} from "./ui.js";
const url = new URL(window.location.href);
const params = new URLSearchParams(url.search);
const logger = new Logger();
let G;
if (params.has("vizonly"))
    document.body.classList.add("vizonly");

if (params.has("noheader"))
    document.body.classList.add("noheader");

if (params.has("graph")){
    const gname = params.get("graph");
    G = new Graph(gname, logger);
    window.onload = async function(){
        G.build().then(() => set_page(G, true));
        console.log("graph", G);
    }
}
else if (params.has("state")){
    let state = JSON.parse(atob(params.get("state"))); 
    console.log("state", state);
    window.onload = async function(){
        G = await Graph.from_state(state, logger);
        set_page(G, false);
        G.onready();
        console.log("graph", G);
    }
}
else{
    logger.error("invalid URL parameters");
    throw new Error("invalid URL parameters");
}
