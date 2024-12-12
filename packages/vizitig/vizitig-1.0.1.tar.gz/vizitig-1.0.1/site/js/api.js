
export class API{
    #fcts = {}
    constructor(href, logger){
        this.href = href;
        this.logger = logger;
    }
    async build(){
        let result = await fetch(this.href);
        if (!result.ok)
              log.error("An error fetching the openapi file");
        let spec = await result.json();
        this.base_fcts = {};
        let that = this;
        for (const [path, desc] of Object.entries(spec.paths))
            for (const [method, subspec] of Object.entries(desc)){
                let name = subspec.operationId;
                if (this[method] == undefined){
                    this[method] = {}
                    this.base_fcts[method] = {}
                }
                this.base_fcts[method][`${name}`] = build_api_point(path, name, subspec, method, this.logger);
                this[method][`on${name}`] = function(result){return result};
                this[method][name] = async function(...args){
                    let result = await that.base_fcts[method][`${name}`](...args);
                    return that[method][`on${name}`](result);
                }
         }
    } 
} 

// api end point can either be called using formData or a list of aguments that will be fed to the url
// The last 
function build_api_point(path, name, spec, method, logger){
    return async function(...args){
        let url = path;
        let i;
        if (args.length == 1 && args[0].constructor == FormData){
            let form = args[0];
            i = 0;
            for (const el of spec.parameters){
                if (el.in == "path"){
                    url = url.replace(/{.*?}/, form.get(el.name));
                    form.delete(el.name);
                }
            }
            if (!spec.requestBody){
                url = `${url}?${new URLSearchParams(form)}`;
            }
        } else {
            for (i=0; i<args.length; i++)
                if (url.search(/{.*?}/) > 0)
                    url = url.replace(/{.*?}/, args[i])
                else
                    break
            
        }
        if (url.search(/{.*?}/) > 0)
            logger.error(`Not enough arguments for ${name}: ${path} with ${args}`);

        if (i< args.length - 1)
            logger.error(`Too much arguments for ${name}: ${path} with ${args}`);

        let body = {
            method: method,
        };

        if (spec.requestBody){
            if (i != args.length-1 && spec.requestBody.required)
                logger.error(`Not enough arguments for ${name}: ${path} with ${args}`);
                let content_types = [...Object.keys(spec.requestBody.content)]
                if (content_types.length > 1)
                    logger.error("unsupported content multiplexing");
                let content_type = content_types[0];
                if (content_type == "application/json"){
                    body["body"] = JSON.stringify(args[args.length-1]);
                    body["headers"] = {
                        "Content-Type": "application/json",
                    }
                }
                else if (content_type == "multipart/form-data"){
                    body["body"] = args[args.length-1];
                }
                else
                    logger.error(`Unspported content type ${content_type}`);
        }
        let result = await fetch(`api${url}`, body);
        console.log("Result");
        console.log(result);
        if (!result.ok){
            let msg;
            if (result.status != 500){
                let body = await result.json();
                msg = body.detail;
            }
            else 
                msg = "Server error";
            logger.error(`API::${msg}`);
            throw new Error(msg);
        }
        return await result.json();
    }
}
