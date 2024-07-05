CREATE TABLE Usuario (
		ID serial,
		nome text NOT NULL,
		email TEXT NOT NULL CHECK (email ~ '^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'),
		genero varchar(1),
		dataNascimento date NOT NULL,
		data timestamp,
		paisOrigem text NOT NULL,
		primary key (ID)
);

CREATE TABLE Canal (
		ID serial,
		nome text NOT NULL,
		apelido text NOT NULL,
		qtdInscritos int DEFAULT 0,
		qtdVideos int DEFAULT 0,
		qtdViews int DEFAULT 0,
		primary key (ID)
);

CREATE TABLE Video (
		ID serial,
		idCanal int,
		titulo text NOT NULL,
		qualidade int NOT NULL CHECK (qualidade IN (144, 240, 360, 480, 720, 1080, 2160)),
		framerate int NOT NULL CHECK (framerate IN (25, 30, 50, 60)),
		data timestamp,
		descricao varchar(500) DEFAULT '',
		qtdGosteis int DEFAULT 0,
		qtdViews int DEFAULT 0,
		visibilidade text DEFAULT 'publico' CHECK (visibilidade IN ('publico', 'nao-listado', 'privado')),
		audiencia text DEFAULT 'todos' CHECK (audiencia IN ('infantil', 'todos')),
		restricaoIdade text DEFAULT 'todos' CHECK (restricaoIdade IN ('adultos', 'todos')),
		primary key (ID),
		foreign key (idCanal) references Canal(ID)
);

CREATE TABLE Comentario (
		ID serial,
		idVideo int,
		idUsuario int,
		texto varchar(300) NOT NULL,
		data timestamp,
		resposta int DEFAULT NULL,
		qtdRespostas int DEFAULT 0,
		coracao boolean DEFAULT FALSE,
		primary key (ID),
		foreign key (idVideo) references Video (ID),
		foreign key (idUsuario) references Usuario (ID)
);

CREATE TABLE UsuarioCanal (
		idUsuario int,
		idCanal int,
		cargo text CHECK (cargo IN ('owner', 'mod', 'editor')),
		primary key (idUsuario, idCanal),
		foreign key (idUsuario) references Usuario (ID),
		foreign key (idCanal) references Canal (ID)
);

CREATE TABLE Inscricao (
		idUsuario int,
		idCanal int,
		data timestamp,
		primary key (idUsuario, idCanal),
		foreign key (idUsuario) references Usuario (ID),
		foreign key (idCanal) references Canal (ID)
);

CREATE TABLE Visualizacao (
		idUsuario int,
		idVideo int,
		data timestamp,
		primary key (idUsuario, idVideo, data),
		foreign key (idUsuario) references Usuario (ID),
		foreign key (idVideo) references Video (ID)
);

CREATE TABLE Gostei (
		idUsuario int,
		idVideo int,
		data timestamp,
		acao boolean,
		primary key (idUsuario, idVideo),
		foreign key (idUsuario) references Usuario (ID),
		foreign key (idVideo) references Video (ID)
);
