from tf.advanced.app import App


class TfApp(App):
    def __init__(app, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fmt_layoutRich(app, n, **kwargs):
        api = app.api
        F = api.F
        after = f'{F.punc.v(n) or ""} '
        isGap = F.gap.v(n)
        material = F.letters.v(n) or ""
        layout = f'<span class="gap">{material}</span>' if isGap else material
        return f"{layout}{after}"
