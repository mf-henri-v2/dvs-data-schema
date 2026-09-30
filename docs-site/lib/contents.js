// Reads the guides and their sections from the contents page,
// schema-1.0/README.md, so that the site keeps no list of its own.
//
// A guide is a heading such as "## GPG 45: identity checking". Its sections
// are the numbered links below it, such as
// "- [3. Data model](gpg-45/03-data-model.md)". tools/check_links.py reads the
// page the same way to check the issue forms.

const GUIDE = /^## (GPG \d+: .+?)\s*$/;
const SECTION = /^- \[(\d+\. [^\]]+)\]\(([^)#]+\.md)\)/;

// The choices the issue forms offer when feedback is not about one guide or
// one section. tools/check_links.py checks the forms against the same words.
export const SUPPORTING_MATERIAL = "Supporting material";
export const OTHER_GUIDE = "Something else, or not sure";
export const NO_SECTION = "Not about a specific section, or not sure";

/** The guides on the contents page: [{ title, folder, sections: [{ label, path }] }]. */
export function readContents(markdown) {
  const guides = [];
  let current = null;
  for (const line of markdown.split(/\r?\n/)) {
    const guide = GUIDE.exec(line);
    const section = SECTION.exec(line);
    if (guide) {
      current = { title: guide[1], folder: "", sections: [] };
      guides.push(current);
    } else if (line.startsWith("## ")) {
      current = null; // any other heading ends the guide's list
    } else if (section && current) {
      current.sections.push({ label: section[1], path: section[2] });
      current.folder ||= section[2].split("/")[0];
    }
  }
  if (!guides.length || guides.some((guide) => !guide.sections.length)) {
    throw new Error("The contents page must list each guide as '## GPG NN: name' followed by its numbered sections.");
  }
  return guides;
}

/** What to choose in an issue form for feedback about a page. */
export function feedbackChoices(found, repoPath) {
  if (found) {
    return { guide: found.guide.title, section: found.section ? found.section.label : NO_SECTION };
  }
  const guide = repoPath.startsWith("supporting-material/") ? SUPPORTING_MATERIAL : OTHER_GUIDE;
  return { guide, section: NO_SECTION };
}
