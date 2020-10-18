<script>
  import { onMount, afterUpdate, beforeUpdate } from "svelte";
  import Card from "./Card.svelte";

  export let data;

  let mj = false;

  onMount(() => {
    let script = document.createElement('script');
    let script_code = document.createTextNode(`
      MathJax = {
        tex: {inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]},
        processEscapes: true
      };
    `);
    script.appendChild(script_code);
    document.head.append(script);

    let mj_script = document.createElement('script');
    mj_script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
    document.head.append(mj_script);
    
    mj_script.onload = () => {
      mj = MathJax;
    }
  });


  let colors = ["#3772ff","#1f1b12","#855251","#5cb695","#ccaa66",
                "#d2b0d4","#7f8a97","#81988c","#392841","#8d8180"];
  
  let root_list_ix = 0;
  let cur_list = data.contents.slice(1);
  let highlighted_ix = 0;
  let prev_lvl_ixs = [];
  let prev_lists = [];
  
  console.log(data);

  $: highlighted = cur_list[highlighted_ix];
  $: level1 = cur_list.slice(highlighted_ix + 1);
  $: level2 = cur_list[highlighted_ix].contents;
  
  function handleKeypress(event) {
    switch(event.key){
      case "ArrowDown":
        if (highlighted_ix < cur_list.length - 1) {
          highlighted_ix++;
          if (prev_lists.length == 0) {
            root_list_ix++;
          }
        }
        break;
      case "ArrowUp":
        if (highlighted_ix > 0) {
          highlighted_ix = highlighted_ix - 1;
          if (prev_lists.length == 0) {
            root_list_ix = root_list_ix - 1;
          }
        }
        break;
      case "ArrowRight":
        if (highlighted.contents && highlighted.contents.length > 0) {
          var new_highlighted_ix = 0;
          var new_list = highlighted.contents;

          while(new_list[new_highlighted_ix].type != "headline") {
            new_highlighted_ix = new_highlighted_ix + 1;
            if (new_highlighted_ix === new_list.length) {
              new_highlighted_ix = -1;
              break;
            }
          }
          if (new_highlighted_ix != -1) {
            prev_lvl_ixs = [...prev_lvl_ixs, highlighted_ix];
            prev_lists = [...prev_lists, cur_list];
            highlighted_ix = new_highlighted_ix;
            cur_list = new_list;
          }

        }
        break;
      case "ArrowLeft":
        if (prev_lists.length > 0) {
          cur_list = prev_lists.pop();
          prev_lists = prev_lists;
          highlighted_ix = prev_lvl_ixs.pop();
          prev_lvl_ixs = prev_lvl_ixs;
        }
    };
  };
  
  $: highlighted_color = colors[root_list_ix];
  
  function make_lvl1_colors(root_list_ix, top_level) {
    var tmp = [];
    for(var i=0; i < level1.length; i++) {
        tmp[i] = colors[(top_level) ? (root_list_ix + i + 1) : root_list_ix];
    }
    return tmp;
  }
  
  beforeUpdate(() => {
    if (mj) {
      //mj.startup.document.state(0); 
      //mj.typesetClear();
      //mj.texReset();
    }
  })

  afterUpdate(() => {
    if (mj) { mj.typeset(); }
  });
  
  $: top_level = (prev_lists.length == 0);
  $: lvl1_colors = make_lvl1_colors(root_list_ix, top_level); 

</script>

<svelte:window on:keydown={handleKeypress}/>

<div id="row">
  <div id="col1" class="col">
    {#key highlighted.ref}
    <Card card={highlighted} _class="card highlighted" color="{highlighted_color}" />
    {/key}
    {#each level1 as card, i (card.ref)}
      <Card card={card} _class="card" color="{lvl1_colors[i]}"/>
    {/each}
  </div>
  <div id="col2" class="col">
    {#each level2 as card (card.ref)}
      <Card card={card} _class="card" color="{highlighted_color}"/>
    {/each}
  </div>
</div>

<style>
    * { 
        -moz-box-sizing: border-box; 
        -webkit-box-sizing: border-box; 
         box-sizing: border-box; 
    }

    #row { display: flex; }
    
    .col {
      flex: 1;
    }
    
</style>
