import pydantic

from src.schemas.newsletter.create import CreateLetter

payload = {
    "title": "testing",
    "genre": "as",
    "body": [
        {
            "subtitle": "titulo 1",
            "content": "Os tupis se espalhavam do atual Rio Grande do Sul ao Rio Grande do Norte de hoje,[33] sendo a primeira raça indígena que teve contato com o colonizador e decorrentemente a de maior presença, com influência no mameluco, no mestiço, no luso-brasileiro que nascia e no europeu que se fixava",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Desembarque_de_Pedro_%C3%81lvares_Cabral_em_Porto_Seguro_em_1500_by_Oscar_Pereira_da_Silva_%281865%E2%80%931939%29.jpg/220px-Desembarque_de_Pedro_%C3%81lvares_Cabral_em_Porto_Seguro_em_1500_by_Oscar_Pereira_da_Silva_%281865%E2%80%931939%29.jpg"
        },
        {
            "subtitle": "titulo 2",
            "content": "Em meados do século XVI, quando o açúcar de cana tornou-se o mais importante produto de exportação do Brasil,[50] os portugueses iniciaram a importação de escravos africanos, comprados nos mercados de escravos da África Ocidental.[51][52] Assim, estes começaram a ser trazidos ao Brasil, inicialmente para lidar com a crescente demanda internacional do produto, naquele que foi denominado ciclo do açúcar",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Replica_da_sede_administrativa_do_Quilombo.jpg/220px-Replica_da_sede_administrativa_do_Quilombo.jpg"
        },
        {
            "content": "Ao final do século XVII, devido à concorrência colonial as exportações de açúcar brasileiro começaram a declinar, mas a descoberta de ouro pelos bandeirantes na década de 1690 abriu um novo ciclo para a economia extrativista da colônia, promovendo uma febre do ouro no Brasil, que atraiu milhares de novos colonos, vindos não só de Portugal, mas também de outras colônias portugu"
        }
    ]
}

try:
    a = CreateLetter(**payload)
    print(a)
except pydantic.ValidationError as e:
    print('error in body, status 422', e)
