/**
 * Adds a page to the given root path.
 * @param {*} rootPath Root path of the page.
 * @param {String} name Name of the page.
 * @param {*} page A Vue Template for the page.
 * @param {String} title A title for the page.
 */
export function activatePage(rootPath, name, page, title) {
  const route = rootPath.children.find((obj) => obj.path === name);
  route.component = page;
  route.meta.title = title;
}
