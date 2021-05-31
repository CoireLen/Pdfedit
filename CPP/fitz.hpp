#include <mupdf/fitz.h>
#include <mupdf/pdf.h>
#include <iostream>
#include <string>
#include <qt5/QtCore/qstring.h>
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
    Doc(QByteArray & qpath);
    ~Doc();
    int pagecount() { return fz_count_pages(ctx, doc); };
    fz_pixmap* GetPageToPixmap(int page_number);
    void save();
    void del_page(int);
    void set_rotation(int,int);
    void DorpPixmap(fz_pixmap* pix);
    void DropDoc();
private:
    Doc();
    QByteArray openfilepath;
    fz_document* doc;
    fz_context* ctx;
    pdf_document* pdf;
};
Doc::Doc(QByteArray &qpath) {
    ctx = fz_new_context(NULL, NULL, FZ_STORE_UNLIMITED);
    if (!ctx)
    {
        printf("\nnew context err\n");
        return;
    }
    fz_try(ctx)
        fz_register_document_handlers(ctx);
    fz_catch(ctx)
    {
        printf("\nreg doc hendler err\n");
        fz_drop_context(ctx);
        return;
    }
    fz_try(ctx) {
        printf("\nfilepath:%s", qpath.data());
        this->doc = fz_open_document(ctx, qpath.data());
        this->openfilepath = qpath;
        this->pdf = pdf_specifics(ctx, doc);
    }
    fz_catch(ctx)
    {
        printf("\ndoc open err\n");
        fz_drop_context(ctx);
        ctx = 0;
        return;
    }
}
fz_pixmap* Doc::GetPageToPixmap(int page_number) {
    return fz_new_pixmap_from_page_number(ctx, doc, page_number, fz_scale(1,1), fz_device_rgb(ctx), 0);
}
void Doc::DorpPixmap(fz_pixmap*pix) {
    fz_drop_pixmap(ctx, pix);
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
        pdf_save_document(ctx, pdf,(const char *)openfilepath.data(), &opts);
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
void Doc::DropDoc() {
  
}
Doc::~Doc()
{
    
    printf("\ndrop pdf doc:");
    pdf_drop_document(ctx, pdf);
    printf("\ndrop doc:");
    fz_drop_document(ctx, doc);
    printf("\ndrop con:");
    fz_drop_context(ctx);
}
