<script>
  import { onMount } from 'svelte';
  import marked from 'marked';
  import frontMatter from 'front-matter';

  import Base from '../Base.svelte';
  import MediaQuery from '../utils/MediaQuery.svelte';
  import CardTree from '../CardTree.svelte';

  export let params;

  const md_root = "/markdown/";
  let data = {body:"", attributes:{title:""}};
  let front_matter = "";
  let mj = null;

  onMount(async () => {
    const md_response = await fetch(md_root + params.id + ".md");
    data = await md_response.text();
    data = frontMatter(data);

    let script = document.createElement('script');
    let script_code = document.createTextNode(`
      MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
          displayMath: [ ['$$','$$'], ['\\\\[','\\\\]'] ]
        },
        startup: {
          ready: function () {
            var math = MathJax._.core.MmlTree.MmlNodes.math.MmlMath;
            math.defaults.scriptminsize = '0px';
            MathJax.startup.defaultReady();
          }
        },
        chtml: {scale: 1},
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

</script>

<Base>
<div class="wrapper">
  <div class="content">
    <h1 class="title">{data.attributes.title}</h1>
    {#if data.attributes.type == 'normal'}
        {@html marked(data.body)}
    {:else if data.attributes.type == 'tree'}
       <CardTree data={data.body} mj={mj} />
    {/if}
  </div>
</div>
</Base>

<style>
  .wrapper {
    max-width: 90%;
    margin: auto;
  }
  .content {
    max-width: 800px;
    padding-top: 1em;
    margin: auto;
    text-align: justify;
  }

  :global(.MathJax) {
    font-size: 1.1em !important;
  }

  :global(h1) {
    font-size: 1.3em;
  }

  :global(h2) {
    font-size: 1.1em;
    font-weight: 500;
  }
</style>
