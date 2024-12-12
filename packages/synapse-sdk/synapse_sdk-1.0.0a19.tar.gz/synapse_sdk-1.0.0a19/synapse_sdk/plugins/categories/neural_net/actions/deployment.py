from synapse_sdk.clients.exceptions import ClientError
from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod


@register_action
class DeploymentAction(Action):
    name = 'deployment'
    category = PluginCategory.NEURAL_NET
    method = RunMethod.JOB

    def get_actor_options(self):
        options = {'runtime_env': self.get_runtime_env()}
        for option in ['num_cpus', 'num_gpus']:
            option_value = self.params.get(option)
            if option_value:
                options[option] = option_value
        return options

    def start(self):
        from ray import serve

        self.ray_init()
        deployment = serve.deployment(ray_actor_options=self.get_actor_options())(self.entrypoint)
        serve.delete(self.plugin_release.code)
        # TODO add run object
        serve.run(deployment.bind(), name=self.plugin_release.code, route_prefix=f'/{self.plugin_release.checksum}')

        # 백엔드에 ServeApplication 추가
        serve_application = self.create_serve_application()
        return {'serve_application': serve_application['id'] if serve_application else None}

    def create_serve_application(self):
        if self.job_id:
            try:
                serve_application = self.ray_client.get_serve_application(self.plugin_release.code)
                return self.client.create_serve_application({
                    'job': self.job_id,
                    'status': serve_application['status'],
                    'data': serve_application,
                })
            except ClientError:
                pass
        return None
