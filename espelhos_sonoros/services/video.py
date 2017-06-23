import flask
VIDEOS = [
    {
        "desc": "O projeto \"Espelho Sonoro\", idealizado pelo sound designer Rodrigo Ramos, pretende o mapeamento de som da ilha de Florian\u00f3polis utilizando de uma releitura de localizadores sonoros ac\u00fasticos usados durante a Primeira Guerra Mundial.\n\nO aparato passou pelo Mirante do Morro da Lagoa da Concei\u00e7\u00e3o, e registrou essa paisagem sonora com a interatividade dos transeuntes.\nSaiba mais no site www.espelhosonoro.com",
        "id": "pCRkeVJTgGg",
        "lat": -27.60084,
        "lng": -48.48132,
        "title": "Espelho Sonoro - Mirante Morro da Lagoa da Concei\u00e7\u00e3o",
        "url": "https://youtube.com/watch?v=pCRkeVJTgGg"
    },
    {
        "desc": "O projeto \"Espelho Sonoro\", idealizado pelo sound designer Rodrigo Ramos, pretende o mapeamento de som da ilha de Florian\u00f3polis utilizando de uma releitura de localizadores sonoros ac\u00fasticos usados durante a Primeira Guerra Mundial.\n\nO aparato passou pelo Largo da Alf\u00e2ndega, no centro da cidade, e registrou essa paisagem sonora com a interatividade dos transeuntes.\nSaiba mais no site www.espelhosonoro.com",
        "id": "j2KRpsIOmaY",
        "lat": -27.59758,
        "lng": -48.55231,
        "title": "Espelho sonoro  Largo da Alfa\u0302ndega",
        "url": "https://youtube.com/watch?v=j2KRpsIOmaY"
    },
    {
        "desc": "O projeto \"Espelho Sonoro\", idealizado pelo sound designer Rodrigo Ramos, pretende o mapeamento de som da ilha de Florian\u00f3polis utilizando de uma releitura de localizadores sonoros ac\u00fasticos usados durante a Primeira Guerra Mundial.\n\nO aparato passou por Sambaqui e registrou essa paisagem sonora com a interatividade dos transeuntes.\nSaiba mais no site www.espelhosonoro.com",
        "id": "PHFK5LD1DVM",
        "lat": -27.48944,
        "lng": -48.53777,
        "title": "Espelho Sonoro   Sambaqui",
        "url": "https://youtube.com/watch?v=PHFK5LD1DVM"
    },
    {
        "desc": "O projeto \"Espelho Sonoro\", idealizado pelo sound designer Rodrigo Ramos, pretende o mapeamento de som da ilha de Florian\u00f3polis utilizando de uma releitura de localizadores sonoros ac\u00fasticos usados durante a Primeira Guerra Mundial.\n\nO aparato passou pelo Parque de Coqueiros, na parte continental da cidade, e registrou essa paisagem sonora.\nSaiba mais no site www.espelhosonoro.com",
        "id": "9PCZ-p75pKA",
        "lat": -27.60176,
        "lng": -48.57407,
        "title": "Espelho Sonoro   Parque Coqueiros",
        "url": "https://youtube.com/watch?v=9PCZ-p75pKA"
    },
    {
        "desc": "O projeto \"Espelho Sonoro\", idealizado pelo sound designer Rodrigo Ramos, pretende o mapeamento de som da ilha de Florian\u00f3polis utilizando de uma releitura de localizadores sonoros ac\u00fasticos usados durante a Primeira Guerra Mundial.\n\nO aparato passou pela Praia Lagoinha, na regi\u00e3o Norte da cidade, e registrou essa paisagem sonora com a interatividade dos transeuntes.\nSaiba mais no site www.espelhosonoro.com",
        "id": "y7m---RgDSc",
        "lat": -27.38911,
        "lng": -48.42119,
        "title": "Espelho Sonoro - Lagoinha",
        "url": "https://youtube.com/watch?v=y7m---RgDSc"
    }]

def video_service(app, socketio, video_dao):

    @app.route('/api/videos', methods=['GET'])
    def list_videos_json():
        return flask.jsonify(VIDEOS)
        #return flask.jsonify(list(map(lambda v: v._asdict(), video_dao.list())))

