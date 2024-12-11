from optrabot.tradetemplate.processor.templateprocessorbase import TemplateProcessorBase
from optrabot.tradetemplate.templatefactory import Template
#from optrabot.tradetemplate.template import Template


class IronFlyProcessor(TemplateProcessorBase):
	
	def __init__(self, template: Template):
		"""
		Initializes the put spread processor with the given template
		"""
		super().__init__(template)