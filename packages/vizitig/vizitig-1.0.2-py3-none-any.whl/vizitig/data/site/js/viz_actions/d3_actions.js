import { VizAction } from "./default_actions.js";


export class ShowId extends VizAction {
    transform_node(nodeid, draw_node){

        if (this.check(nodeid)){

            let scale = this.args.get("scale"); 
            draw_node.select(".add_info").append("text")
                     .text(nodeid)
                     .attr("fill", "black")
                     .attr("stroke-width", "0px")
                     .attr("stroke", "black")
                     .attr("x", "-1.6em")
                     .attr("y", "1.35em")
                     .style("font-size", "xx-small")
                     .attr("transform", `scale(${scale} ${scale})`);
        }
        return draw_node;
    }
    static get form_desc() {
        return [
            {
                type: "number", 
                min: "0.1",
                max: "10",
                step: "0.1",
                name: "scale",
                label: "Scale",
                required: "",
                value: "1",
            }
        ];
    }
}

export class Scale extends VizAction {
    transform_node(nodeid, draw_node){
        if (this.check(nodeid)){
            let tr = draw_node.attr("transform");
            if (tr == null)
                tr = "";
            let scale = this.args.get("scale"); 
            draw_node.attr("transform", `${tr} scale(${scale} ${scale})`);
        }
        return draw_node;
    }

    static get form_desc() {
        return [
            {
                type: "number", 
                min: "0.1",
                max: "10",
                step: "0.1",
                name: "scale",
                label: "Scale",
                required: "",
                value: "1",
            }
        ];
    }
}

export class Transparency extends VizAction{
    transform_node(nodeid, draw_node){
        if (this.check(nodeid)){
            draw_node.attr("fill-opacity", this.args.get("alpha"))
                .attr("stroke-opacity", this.args.get("alpha"));
        }
        return draw_node;
    }

    transform_edge(source, target, draw_edge){
        if (this.check(source) || this.check(target)){
            draw_edge.attr("stroke-opacity", this.args.get("alpha"));
        }
        return draw_edge;
    }

    static get form_desc() {
        return [
            {
                type: "range", 
                min: "0",
                max: "1",
                step: "0.05",
                name: "alpha",
                required: "",
                label: "Transparency"
            }
        ];
    }
}

class DefaultHighlight extends VizAction{
    transform_node(nodeid, draw_node){
        if (this.check(nodeid))
            draw_node.attr("fill", this.args.get("color"));
        return draw_node;
    }

    static get form_desc() {
        return [
            {
                type: "color", 
                name: "color",
                required: "",
                label: "Color"
            }
        ];
    }

}

export class Highlight extends DefaultHighlight {

    transform_edge(source, target, draw_edge){
        if (this.check(source) & this.check(target)){
            draw_edge.attr("stroke", this.args.get("color"))
                .attr("stroke-width", this.args.get("edgew"));
        }
        return draw_edge;
    }

    static get form_desc() {
        let T = super.form_desc;
        T.push({
            type: "number", 
            min: "1",
            max: "10",
            name: "edgew",
            label: "Edge width"
        });
        return T;
    }
}

export class Tag extends DefaultHighlight {
    transform_node(nodeid, draw_node){
        let tag_size = parseInt(this.args.get("tag_size"));
        if (this.check(nodeid)){
            if (draw_node.tag_left == undefined)
                draw_node.tag_left = 0;
            draw_node.select(".add_info").append("circle")
                     .attr("r", tag_size)
                     .attr("fill",this.args.get("color"))
                     .attr("transform", `translate(${tag_size + draw_node.tag_left}, 0)`);
            draw_node.tag_left += tag_size; 
        }
        return draw_node;
    }

    static get form_desc() {
        let T = super.form_desc;
        T.push({
            type: "number", 
            min: "4",
            max: "10",
            name: "tag_size",
            label: "Size",
            value: "4",
            required: "",
        });
        return T;
    }
}
