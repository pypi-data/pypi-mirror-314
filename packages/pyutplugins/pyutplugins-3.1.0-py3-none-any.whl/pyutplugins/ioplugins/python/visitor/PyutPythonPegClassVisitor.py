
from typing import List

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype

from pyutplugins.ioplugins.python.visitor.ParserTypes import ParentName
from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClassName
from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClasses
from pyutplugins.ioplugins.python.visitor.ParserTypes import VERSION

from pyutplugins.ioplugins.python.pythonpegparser.PythonParser import PythonParser
from pyutplugins.ioplugins.python.visitor.PyutBaseVisitor import NO_CLASS_DEF_CONTEXT

from pyutplugins.ioplugins.python.visitor.PyutBaseVisitor import PyutBaseVisitor


ENUMERATION_SUPER_CLASS: str = 'Enum'


class PyutPythonPegClassVisitor(PyutBaseVisitor):
    """
    Simply does a scan to identify all the classes;   A separate
    is needed to do inheritance
    """

    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    @property
    def pyutClasses(self) -> PyutClasses:
        return self._pyutClasses

    @pyutClasses.setter
    def pyutClasses(self, pyutClasses: PyutClasses):
        self._pyutClasses = pyutClasses

    def visitClass_def(self, ctx: PythonParser.Class_defContext):
        """
        Visit a parse tree produced by PythonParser#class_def.

        Args:
            ctx:
        """
        #
        # Check if we are an enumeration
        #
        className: PyutClassName = self._extractClassName(ctx=ctx)

        pyutClass: PyutClass = PyutClass(name=className)
        pyutClass.description = self._generateMyCredits()

        argumentsCtx: PythonParser.ArgumentsContext = self._findArgListContext(ctx)

        if argumentsCtx is not None:
            args: PythonParser.ArgsContext = argumentsCtx.args()
            parentName: ParentName = ParentName(args.getText())
            self.logger.debug(f'Class: {className} is subclass of {parentName}')
            parents: List[str] = parentName.split(',')
            for parent in parents:
                if parent == ENUMERATION_SUPER_CLASS:
                    pyutClass.stereotype = PyutStereotype.ENUMERATION
                    break

        self._pyutClasses[className] = pyutClass

        return self.visitChildren(ctx)

    def visitPrimary(self, ctx: PythonParser.PrimaryContext):
        """
        If it is an assignment inside a class marked as an enumeration, then
        create Fields to emulate the enumeration

        Args:
            ctx:
        """
        primaryStr: str = ctx.getText()
        if primaryStr.startswith('NewType'):
            argumentsCtx: PythonParser.ArgumentsContext = ctx.arguments()
            if argumentsCtx is not None:

                argStr = ctx.children[2].getText()
                typeValueList = argStr.split(',')
                self.logger.debug(f'{typeValueList=}')

                className = typeValueList[0].strip("'").strip('"')
                self.logger.debug(f'{className}')

                pyutClass: PyutClass = PyutClass(name=className)

                pyutClass.description = self._generateMyCredits()
                pyutClass.stereotype  = PyutStereotype.TYPE

                self._pyutClasses[className] = pyutClass

        return self.visitChildren(ctx)

    def visitAssignment(self, ctx: PythonParser.AssignmentContext):
        """
        Visit a parse tree produced by PythonParser#assignment.

        Args:
            ctx:
        """
        if self._isThisAssignmentInsideAMethod(ctx=ctx) is False:

            classCtx:  PythonParser.Class_defContext = self._extractClassDefContext(ctx)
            if classCtx == NO_CLASS_DEF_CONTEXT:
                pass
            else:
                className: PyutClassName                 = self._extractClassName(ctx=classCtx)
                pyutClass: PyutClass                     = self._pyutClasses[className]
                if pyutClass.stereotype == PyutStereotype.ENUMERATION:
                    if len(ctx.children) >= 2:
                        enumName:     str = ctx.children[0].getText()
                        defaultValue: str = ctx.children[2].getText()
                        self.logger.info(f'')
                        self._makeFieldForClass(className=className, propertyName=enumName, typeStr='', defaultValue=defaultValue)

        return self.visitChildren(ctx)

    def _generateMyCredits(self) -> str:
        """

        Returns:    Reversed Engineered by the one and only:
                    Gato Malo - Humberto A. Sanchez II
                    Generated: ${DAY} ${MONTH_NAME_FULL} ${YEAR}
                    Version: ${VERSION}

        """
        from datetime import date

        today: date = date.today()
        formatDated: str = today.strftime('%d %B %Y')

        hasiiCredits: str = (
            f'Reversed Engineered by the one and only:{osLineSep}'
            f'Gato Malo - Humberto A. Sanchez II{osLineSep}'
            f'Generated: {formatDated}{osLineSep}'
            f'Version: {VERSION}'
        )

        return hasiiCredits
