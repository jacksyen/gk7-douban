var Main = {
	data() {
		var validateUserEmail = (rule, value, callback) => {
			if (this.setForm.switchKindle) {
				if (value === '') {
					callback(new Error('请输入邮箱前缀'));
				}
			}
			callback();
		};
		return {
			setForm: {
				switchKindle: localStorage.SWITCH_KINDLE=='true'?true:false,
                kindleItemDisabled: localStorage.SWITCH_KINDLE=='true'?false:true,
				privateEmail: localStorage.TO_PRIVATE_MAIL,
				userEmail: localStorage.TO_MAIL?localStorage.TO_MAIL.split('@')[0] : '',
				emailDomain: localStorage.TO_MAIL?'@'+localStorage.TO_MAIL.split('@')[1] : '@kindle.com',
				kindleEnd: [
					'@kindle.com',
					'@free.kindle.com',
					'@kindle.cn',
					'@iduokan.com'
				],
				whiteMail : [
					'gk7.douban@gmail.com',
					'gk7.douban1@gmail.com',
					'gk7.douban2@gmail.com'
				]
			},
			rules: {
				privateEmail: [
					{ required: true, message: '请输入邮箱地址', trigger: 'blur' },
					{ type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
				],
				userEmail: [
					{ validator: validateUserEmail, trigger: 'blur' }
				]

			}
		}
	},
	methods: {
        changeSwitchKindle() {
			this.setForm.kindleItemDisabled=!this.setForm.switchKindle;
		},
		submitForm(formName) {
			this.$refs[formName].validate((valid) => {
				if (valid) {
					if (this.setForm.switchKindle===true) {
						var kindleEmail = this.setForm.userEmail+this.setForm.emailDomain;
						localStorage.TO_MAIL = kindleEmail;
						localStorage.SWITCH_KINDLE = true;
					} else {
						localStorage.TO_MAIL = '';
						localStorage.SWITCH_KINDLE = false;
					}
					localStorage.TO_PRIVATE_MAIL = this.setForm.privateEmail;
					console.log('TO_MAIL:'+localStorage.TO_MAIL+",SWITCH_KINDLE:"+localStorage.SWITCH_KINDLE+",TO_PRIVATE_MAIL:"+localStorage.TO_PRIVATE_MAIL);
                    this.$message({
                        message: '修改成功',
                        type: 'success'
                    });
					return;
				}
				return false;

			});
		}
	}
};
var Ctor = Vue.extend(Main);
new Ctor().$mount('#app');

