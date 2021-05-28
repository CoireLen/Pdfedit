#include <mupdf/fitz.h>
#include <mupdf/pdf.h>
#include <iostream>
#include <string>
#include <qt5/QtCore/qstring.h>
pdf_annot* JM_get_annot_by_name(fz_context* ctx, pdf_page* page, char* name)
{
    if (!name || strlen(name) == 0) {
        return NULL;
    }
    pdf_annot** annotptr = NULL;
    pdf_annot* annot = NULL;
    int found = 0;
    size_t len = 0;

    fz_try(ctx) {   // loop thru MuPDF's internal annots and widget arrays
        for (annotptr = &page->annots; *annotptr; annotptr = &(*annotptr)->next) {
            annot = *annotptr;
            const char* response = pdf_to_string(ctx, pdf_dict_gets(ctx, annot->obj, "NM"), &len);
            if (strcmp(name, response) == 0) {
                found = 1;
                break;
            }
        }
        if (!found) {
            fz_throw(ctx, FZ_ERROR_GENERIC, "'%s' is not an annot of this page", name);
        }
    }
    fz_catch(ctx) {
        fz_rethrow(ctx);
    }
    return pdf_keep_annot(ctx, annot);
}
pdf_annot* JM_get_annot_by_xref(fz_context* ctx, pdf_page* page, int xref)
{
    pdf_annot** annotptr = NULL;
    pdf_annot* annot = NULL;
    int found = 0;
    size_t len = 0;

    fz_try(ctx) {   // loop thru MuPDF's internal annots array
        for (annotptr = &page->annots; *annotptr; annotptr = &(*annotptr)->next) {
            annot = *annotptr;
            if (xref == pdf_to_num(ctx, annot->obj)) {
                found = 1;
                break;
            }
        }
        if (!found) {
            fz_throw(ctx, FZ_ERROR_GENERIC, "xref %d is not an annot of this page", xref);
        }
    }
    fz_catch(ctx) {
        fz_rethrow(ctx);
    }
    return pdf_keep_annot(ctx, annot);
}
class Page
{
public:
    ~Page();

private:

};
Page::~Page()
{
}
class Doc
{
public:
    Doc(QString);
    ~Doc();
    int pagecount() { return fz_count_pages(ctx, doc); };
    fz_pixmap* GetPageToPixmap(int page_number);
    void save();
    void del_page(int);
    void set_rotation(int,int);
private:
    Doc();
    QString openfilepath;
    fz_document* doc;
    fz_context* ctx;
    pdf_document* pdf;
};
Doc::Doc(QString qpath) {
    ctx = fz_new_context(NULL, NULL, FZ_STORE_UNLIMITED);
    if (!ctx)
    {
        return;
    }
    fz_try(ctx)
        fz_register_document_handlers(ctx);
    fz_catch(ctx)
    {
        fz_drop_context(ctx);
        return;
    }
    fz_try(ctx) {
        doc = fz_open_document(ctx, (char*)qpath.toStdString().c_str());
        openfilepath = qpath;
        pdf = pdf_specifics(ctx, doc);
    }
    fz_catch(ctx)
    {
        fz_drop_context(ctx);
        return;
    }
}
fz_pixmap* Doc::GetPageToPixmap(int page_number) {
    return fz_new_pixmap_from_page_number(ctx, doc, page_number, fz_scale(1,1), fz_device_rgb(ctx), 0);
}
void Doc::save() {
    fz_try(ctx) {
        pdf_write_options opts;
        opts.do_incremental = 1;
        opts.do_ascii = 0;
        opts.do_compress = 0;
        opts.do_compress_images = 0;
        opts.do_compress_fonts = 0;
        opts.do_decompress = 0;
        opts.do_garbage = 0;
        opts.do_pretty = 0;
        opts.do_linear = 0;
        opts.do_clean = 0;
        opts.do_sanitize = 0;
        opts.do_encrypt = 0;
        opts.permissions = -1;
        pdf_save_document(ctx, pdf,(const char *)openfilepath.toStdString().c_str(), &opts);
    }
    fz_catch(ctx) {
        printf("Save Error");
    }
}

void Doc::set_rotation(int rotate=0,int pagenum=0) {
    pdf_page* page = pdf_page_from_fz_page(ctx, fz_load_page(ctx, doc, pagenum));
    int rot = rotate+ pdf_dict_get_int(ctx, page->obj, PDF_NAME(Rotate));
    while (rot < 0) rot += 360;
    while (rot >= 360) rot -= 360;
    //if (type == PDF_ANNOT_FREE_TEXT && rot % 90 != 0)
     //   rot = 0;
    pdf_dict_put_int(ctx, page->obj, PDF_NAME(Rotate), rot);
    
}
void Doc::del_page(int page) {
    pdf_delete_page(ctx, pdf, page);
    if (pdf->rev_page_map)
    {
        pdf_drop_page_tree(ctx, pdf);
    }
}
Doc::~Doc()
{
    
}
