from pomarkdown.core.MarkdownType import MainMarkdown

mainMarkdown = MainMarkdown()


# @except_dec()
def markdown_link_image_to_base64(markdown_path):
    mainMarkdown.markdown_link_image_to_base64(markdown_path)


# @except_dec()
def check_local_dir_image_link_markdown(markdown_path, image_path):
    mainMarkdown.check_local_dir_image_link_markdown(markdown_path, image_path)


def excel2markdown(input_file, output_file=r'./excel2markdown.md', sheet_name=None):
    mainMarkdown.excel2markdown(input_file, output_file, sheet_name)
