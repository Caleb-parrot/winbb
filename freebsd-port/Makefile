PORTNAME=	winbb
DISTVERSIONPREFIX=	v
DISTVERSION=	0.1.0
CATEGORIES=	games

MAINTAINER=	288791519+Caleb-parrot@users.noreply.github.com
COMMENT=	Bible trivia baseball (1994 WinBB remake)
WWW=		https://github.com/Caleb-parrot/winbb

LICENSE=	POLYFORMNC
LICENSE_NAME=	PolyForm Noncommercial License 1.0.0
LICENSE_FILE=	${WRKSRC}/LICENSE
LICENSE_PERMS=	dist-mirror no-dist-sell pkg-mirror no-pkg-sell auto-accept

USES=		desktop-file-utils gl go:modules xorg
GO_MODULE=	github.com/caleb-parrot/winbb
GO_TARGET=	.:winbb
CGO_ENABLED=	0
GO_BUILDFLAGS=	-gcflags=github.com/ebitengine/purego/internal/fakecgo=-std

# Ebitengine v2.10 loads these at runtime (pure Go / purego).
USE_GL=		gl
USE_XORG=	x11 xcursor xi xinerama xrandr xrender xext

PLIST_FILES=	bin/winbb \
		share/applications/winbb.desktop \
		share/icons/hicolor/128x128/apps/bible-baseball.png \
		share/pixmaps/bible-baseball.png

post-install:
	${INSTALL_DATA} ${WRKSRC}/winbb.desktop \
		${STAGEDIR}${PREFIX}/share/applications
	${MKDIR} ${STAGEDIR}${PREFIX}/share/icons/hicolor/128x128/apps
	${INSTALL_DATA} ${WRKSRC}/assets/icon.png \
		${STAGEDIR}${PREFIX}/share/icons/hicolor/128x128/apps/bible-baseball.png
	${MKDIR} ${STAGEDIR}${PREFIX}/share/pixmaps
	${INSTALL_DATA} ${WRKSRC}/assets/icon.png \
		${STAGEDIR}${PREFIX}/share/pixmaps/bible-baseball.png

.include <bsd.port.mk>
