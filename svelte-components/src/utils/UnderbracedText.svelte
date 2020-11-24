<script>
  export let content;
  export let under_content;
  export let bracket_color;
  export let text_color;
</script>

<span style="--bracket-color: {bracket_color}: --text-color: {text_color}" data-bracket="{under_content}">{content}</span>

<style>
span {
  height: 2em;
}
[data-bracket] {
  display: inline-block;
  vertical-align: top;
  position: relative;
}
[data-bracket]:after {
  content: "";
  display: block;
  height: 3px;
  border: 2px solid black;
  border-top: none;
}
[data-bracket]:before {
  content: attr(data-bracket);
  position: absolute;
  top: 70%;
  font-size: 60%;
  color: var(--color);
  padding: 0px;
  white-space: nowrap;
  left: 50%;
  transform: translateX(-50%)
}
</style>
