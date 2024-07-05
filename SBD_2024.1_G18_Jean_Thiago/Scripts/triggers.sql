CREATE OR REPLACE FUNCTION atualizar_quantidade_visualizacoes_canal()
RETURNS TRIGGER AS $$
BEGIN
	IF (TG_OP = 'INSERT') THEN
		UPDATE canal SET qtdviews = qtdviews + 1 WHERE id = (SELECT idCanal FROM video WHERE id = NEW.idVideo);
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION atualizar_quantidade_inscritos_canal()
RETURNS TRIGGER AS $$
BEGIN
	IF (TG_OP = 'INSERT') THEN
		UPDATE canal SET qtdinscritos = qtdinscritos + 1 WHERE id = NEW.idCanal;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION atualizar_quantidade_videos_canal()
RETURNS TRIGGER AS $$
BEGIN
	IF (TG_OP = 'INSERT') THEN
		UPDATE canal SET qtdvideos = qtdvideos + 1 WHERE id = NEW.idCanal;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION atualizar_quantidade_respostas_comentario()
RETURNS TRIGGER AS $$
BEGIN
	IF (TG_OP = 'INSERT' AND NEW.resposta IS NOT NULL) THEN
		UPDATE comentario SET qtdrespostas = qtdrespostas + 1 WHERE id = NEW.resposta;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION atualizar_quantidade_visualizacoes_video()
RETURNS TRIGGER AS $$
BEGIN
	IF (TG_OP = 'INSERT') THEN
		UPDATE video SET qtdviews = qtdviews + 1 WHERE id = NEW.idVideo;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION atualizar_quantidade_gostei_video()
RETURNS TRIGGER AS $$
BEGIN
	IF (TG_OP = 'INSERT') THEN
		UPDATE video SET qtdGosteis = qtdGosteis + 1 WHERE id = NEW.idVideo;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER atualizar_quantidade_visualizacoes_canal_trigger AFTER INSERT ON visualizacao FOR
EACH ROW EXECUTE PROCEDURE atualizar_quantidade_visualizacoes_canal ();

CREATE OR REPLACE TRIGGER atualizar_quantidade_inscritos_canal_trigger AFTER INSERT ON inscricao FOR
EACH ROW EXECUTE PROCEDURE atualizar_quantidade_inscritos_canal ();

CREATE OR REPLACE TRIGGER atualizar_quantidade_videos_canal_trigger AFTER INSERT ON video FOR
EACH ROW EXECUTE PROCEDURE atualizar_quantidade_videos_canal ();

CREATE OR REPLACE TRIGGER atualizar_quantidade_respostas_comentario_trigger AFTER INSERT ON comentario FOR
EACH ROW EXECUTE PROCEDURE atualizar_quantidade_respostas_comentario ();

CREATE OR REPLACE TRIGGER atualizar_quantidade_visualizacoes_video_trigger AFTER INSERT ON visualizacao FOR
EACH ROW EXECUTE PROCEDURE atualizar_quantidade_visualizacoes_video ();

CREATE OR REPLACE TRIGGER atualizar_quantidade_gostei_video_trigger AFTER INSERT ON gostei FOR
EACH ROW EXECUTE PROCEDURE atualizar_quantidade_gostei_video ();