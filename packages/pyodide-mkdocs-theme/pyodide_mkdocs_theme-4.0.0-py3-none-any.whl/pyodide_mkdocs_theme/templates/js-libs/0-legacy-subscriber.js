/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/

/*
-------------------------
     GENERATED FILE
  (see mkdocs_hooks.py)
-------------------------

This module is loaded as "text/javascript", for backward compatibility, providing globals to
avoid failure of old codes.

Purposes/notes:

  - hooks files using subscribeWhenReady

  - MathJax replacements through custom_dir override. Note that, in addition to keep backward
    compatibility, loading mathjax-libs.js in a synch way also simplifies A LOT getting everything
    right at load time (because the mathjax cdn is loaded sync...)

  - The functions defined here are available in the global scope, but won't override the ones
    defined in the modules: those are explicitly imported where needed, in the modules.
    On the other hand, jsLogger becomes unusable in non modules...

  - The modules will override this globals with their own once they are loaded
*/


/**Swallow any kind of call left in a previous version of the theme, in scripts
 * loaded synchronously.
 * */
const jsLogger=()=>null


/**Auto-subscription routine to document changes.
 * If the subscription is not possible yet (readyForSubscription[waitOn] is falsy), try again
 * @delay later until it works.
 *
 * @waitId :  Property to observe in readyForSubscription global object.Also used as subscription
 *            identifier.
 * @callback: Routine to run when the document changes
 * @options : An object with optional fields:
 *      .delay (=50): Time interval (in ms) to wait in between two subscription attempts.
 *      .now (=false): If true, ignore the CONFIG.subscriptionReady property and subscribe at call
 *              time. If false, a callback will be returned by the `subscribeWhenReady` function,
 *              that the caller can use to signal when the subscription is ready.
 *      .waitFor (=null): If given, it must be a boolean provider or a jquery identifier string,
 *              which will result in a function checking for the existence of that element in
 *              the DOM. This function will be called every .delay ms and the subscription will
 *              be delayed until it returns true. This has precedence over the .now option.
 *      .runOnly: if truthy, run the callback when ready, but do not subscribe to document changes.
 *      .maxTries: if not given 20 tries allowed.
 *
 * @throws: Error if maxTries subscriptions attempts are done without success.
 * */
function subscribeWhenReady(waitId, callback, options={}){

    let {now, delay, waitFor, runOnly, maxTries} = {
        delay: 50,
        now: false,
        waitFor: null,
        runOnly: false,
        maxTries: 20,
        ...options
    }
    now = now && !waitFor                       // has to wait if waitFor is used
    CONFIG.subscriptionReady[waitId] = now

    const buildCheckReady=()=>{
        if(!waitFor){
            return ()=>null
        }
        if(typeof (waitFor)=='string'){
            return ()=>{ CONFIG.subscriptionReady[waitId] = $(waitFor).length > 0 }
        }
        return ()=>{ CONFIG.subscriptionReady[waitId] = waitFor() }
    }
    const checkReady = buildCheckReady()
    const isNotReady =()=>{
        checkReady()
        return !CONFIG.subscriptionReady[waitId] || !globalThis.document$
    }

    function autoSubscribe(){

        if(isNotReady()){
            const nTries = CONFIG.subscriptionsTries[waitId]+1 || 1
            if(nTries==maxTries){
                throw new Error(`Impossible to subscribe to ${ waitId } in time: too many tries.`)
            }
            CONFIG.subscriptionsTries[waitId] = nTries
            setTimeout(autoSubscribe, delay)

        }else{
            jsLogger('[Subscribing] -', waitId)
            const wrapper=function(){
                try{
                    callback()
                }catch(e){
                    console.error(e)
                }
            }
            if(runOnly){
                wrapper()
            }else{
                const subscript = document$.subscribe(wrapper)
                document.addEventListener(CONFIG.onDoneEvent, function(){
                    jsLogger("[Unsubscribing] -", waitId)
                    subscript.unsubscribe()
                })
            }
        }
    }
    autoSubscribe()

    if(!now){
        return ()=>{ CONFIG.subscriptionReady[waitId]=true }
    }
}
// TOKEN: end subscribeWhenReady
