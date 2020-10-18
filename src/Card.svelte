<script>
  export let card;
  export let color;
  export let _class;

  function concatenate_paragraph(paragraph) {
    var res = "";
    for (var i=0, len=paragraph.contents.length; i<len; i++) {
      var part = paragraph.contents[i];
      if (typeof part === 'string' || part instanceof String) {
        res = res + part.replace("\n", "<br>");
      } else if (part.type === "link") {
        var caption = "";
        if (part.contents.length > 0) {
          caption = part.contents[0];
        } else {
          caption = part.properties['raw-link'];
        }
        res = res + '<a href="' + part.properties['raw-link'] + '">' + caption + '</a> ';
      } else if (part.type === "latex-fragment") {
        var latex = part.properties.value.replace("$", "\\(");
        latex = latex.replace("$", "\\)");
        res = res + latex + " ";
      }
    }
    return res;
  };

  function concatenate_list(list) {
    var res = "";
    for (var i=0, len=list.contents.length; i<len; i++) {
      var part = list.contents[i];
      if (part.contents[0].type === 'paragraph') {
        part = concatenate_paragraph(part.contents[0]);
        res = res + "* " + part.replace("<br>", "") + "<br>";
      }
    }
    return res;
  }

</script>

{#if card.type === "headline"}
<div class="{_class}" style="background-color: {color}">
    {#if (typeof card.properties.title[0] === 'string' || card.properties.title[0] instanceof String)}
      <h2>{card.properties['raw-value']}</h2>
    {:else if card.properties.title[0].type === 'link'}
      <h2><a href="{card.properties.title[0].properties.path}">{card.properties.title[0].contents[0]}</a></h2>
    {/if}
    {#if card.contents.length > 0}
      {#if card.contents[0].type === "section"}
        {#each card.contents[0].contents as paragraph}
          {#if paragraph.type === "paragraph"}
            <p> {@html concatenate_paragraph(paragraph)} </p>
          {:else if paragraph.type === "plain-list"}
            <p> {@html concatenate_list(paragraph)} </p>
          {/if}
        {/each}
      {/if}
    {/if}
</div>
{/if}

<style>
.card {
  display: block;
  border: solid;
  margin: 1em;
  padding: 0.2em 1em 1em 1em;
  text-size: 20px;
  border-width: 1px;
}
.highlighted {
  border-width: 5px;
}
h2 {
  margin-top: 0.5em;
}

h2 a {
  color: #fff;
  text-decoration: underline;
}
 
</style>
